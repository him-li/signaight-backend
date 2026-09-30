import json
from asyncer import asyncify
import httpx
import asyncio, hashlib, orjson
from typing import List, Optional
import redis.asyncio as redis
from core.logging import logger
from core.config import settings

# --- config ---
_IMGQ_TTL_SECONDS = 86400000 
_IMGQ_LOCK_TIMEOUT = 30
_REDIS_URL = settings.REDIS_URI


def compute_image_quality(meta_data, url, known_tokens, headers={}):
    """
    main function for image quality

    meta_data = {
        "destination": ["s3://testing/dist/1.jpg", "s3://testing/dist/2.jpg"]
    }

    url = "http://127.0.0.1:8000/face/get_image_quality"
    """
    try:
        payload = {}

        files = [
            ('file', (
                'test_s3_.json',
                json.dumps(meta_data),
                'application/json'))
        ]

        headers["Authorization"] = f'Bearer {known_tokens}'
        print("Computing image quality.............")

        timeout = httpx.Timeout(120.0, read=120.0)
        client = httpx.Client(timeout=timeout)
        response = client.post(
            url,
            headers=headers,
            data=payload,
            files=files
        )

        print("Computing image quality finished.............")

        return response.json()
    except Exception as e:
        print(f"Error computing image quality....... {str(e)}")

# --- lazy global redis client ---
_redis_client: Optional[redis.Redis] = None
_redis_lock = asyncio.Lock()

async def _get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client:
        return _redis_client
    async with _redis_lock:
        if not _redis_client:
            _redis_client = redis.from_url(_REDIS_URL, decode_responses=False)
        return _redis_client

def _mk_key(destinations: List[str]) -> str:
    payload = {"destinations": destinations}
    blob = orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
    return hashlib.sha256(blob).hexdigest()

def _redis_keys_for(k: str, prefix = 'imgq') -> tuple[str, str]:
    return (f"{prefix}:{k}", f"{prefix}:lock:{k}")

async def _redis_get_json(r, key: str):
    raw = await r.get(key)
    return orjson.loads(raw) if raw else None

async def _redis_set_json(r, key: str, val: dict, ttl: int):
    await r.set(key, orjson.dumps(val), ex=ttl)
    
EMPTY_IMAGE_QUALITY_RESPONSE = {
            "empty": {
                "scores": {
                    "face_score": 0,
                    "face_count_score": 1,
                    "portrait_score": 1.0,
                    "posture_score": 1.0,
                    "artifacts_score": 0,
                }
            }
        }


# --- main cached function ---
async def get_image_quality_cached(
    data: dict,
    headers: dict,
):
    r = await _get_redis()
    destinations = list((data or {}).get("destination") or [])
    key_hash = _mk_key(destinations)
    cache_key, lock_key = _redis_keys_for(key_hash)

    cached = await _redis_get_json(r, cache_key)
    print('cache key', cache_key)
    if cached is not None:
        if cached.get("Error"):
            return EMPTY_IMAGE_QUALITY_RESPONSE
        return cached

    lock = r.lock(lock_key, timeout=_IMGQ_LOCK_TIMEOUT)
    got_lock = await lock.acquire(blocking=False)

    if got_lock:
        try:
            cached = await _redis_get_json(r, cache_key)
            if cached is not None:
                return cached

            resp = await asyncify(compute_image_quality)(
                        data,
                        f"{settings.FACE_COMPARE_BASE_URL}/face/get_image_quality",
                        settings.FACE_COMPARE_API_KEY,
                        headers
                    )
            if resp.get('Error'):
                resp = EMPTY_IMAGE_QUALITY_RESPONSE
            await _redis_set_json(r, cache_key, resp, _IMGQ_TTL_SECONDS)
            return resp
        finally:
            try:
                await lock.release()
            except Exception:
                pass
            
def compute_face_compare(meta_data, url, known_tokens, headers={}):
    """
    main function for face compare

    meta_data = {
        "source": "s3://testing/source/1.jpg",
        "destination": ["s3://testing/dist/1.jpg", "s3://testing/dist/2.jpg"]
    }

    url = "http://127.0.0.1:8000/face/compare_batch"
    """
    try:
        payload = {}

        files = [
            ('file', (
                'test_s3_.json',
                json.dumps(meta_data),
                'application/json'))
        ]

        headers["Authorization"] = f'Bearer {known_tokens}'
        print("Computing face compare.............")

        timeout = httpx.Timeout(500.0, read=450.0)
        client = httpx.Client(timeout=timeout)
        response = client.post(
            url,
            headers=headers,
            data=payload,
            files=files
        )

        print("Computing face compare finished.............")

        return response.json()
    except Exception as e:
        print(f"Error computing face compare....... {str(e)}")
            
async def compare_images_with_cache(
    data: dict,
    headers: dict,
):
    r = await _get_redis()
    destinations = list((data or {}).get("destination") or [])
    destinations = list((data or {}).get("source") or []) + destinations
    key_hash = _mk_key(destinations)
    cache_key, lock_key = _redis_keys_for(key_hash, "img_compare_data")

    cached = await _redis_get_json(r, cache_key)
    logger.info(f"Retrieved cached compare data for key: {cache_key}")
    if cached is not None:
        return cached

    lock = r.lock(lock_key, timeout=_IMGQ_LOCK_TIMEOUT)
    got_lock = await lock.acquire(blocking=False)

    if got_lock:
        try:
            cached = await _redis_get_json(r, cache_key)
            if cached is not None:
                return cached

            resp = await asyncify(compute_face_compare)(
                data,
                f"{settings.FACE_COMPARE_BASE_URL}/face/compare_batch",
                settings.FACE_COMPARE_API_KEY,
                headers
            )
            image_similarity: dict[str, float] = {
                image: meta["similarity"]
                for image, meta in zip(data.get("destination", []), resp)
                if meta
                and isinstance(meta.get("similarity"), (int, float))
                and meta["similarity"] >= 0
                and "warning" not in meta
            }
            image_similarity_sorted = dict(
                sorted(
                    image_similarity.items(),
                    key=lambda item: item[1],
                    reverse=True
                )
            )
            finally_resp = {'sorted':image_similarity_sorted, 'response': resp, 'data': data, 'headers': headers}
            await _redis_set_json(r, cache_key, finally_resp, _IMGQ_TTL_SECONDS)
            return finally_resp
        finally:
            try:
                await lock.release()
            except Exception:
                pass
