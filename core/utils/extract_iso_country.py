from typing import Any, Optional, List
from core.clients.mapbox.client import api as mapbox_api



def extract_text_values(obj: Any, skip_keys: Optional[List[str]] = None) -> List[str]:
    """
    Recursively extract all string values from nested dict/list objects,
    skipping certain keys (like 'check_ins').
    """
    if skip_keys is None:
        skip_keys = []

    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in skip_keys:
                continue
            results.extend(extract_text_values(v, skip_keys))
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            results.extend(extract_text_values(v, skip_keys))
    elif isinstance(obj, str):
        results.append(obj.strip())
    return results


def looks_like_location(text: str) -> bool:
    """
    Simple heuristic filter to find location-like strings.
    """
    location_keywords = [
        "street", "st ", "road", "rd", "city", "country", "avenue", "ave",
        "district", "region", "state", "zip", "postcode",
        "israel", "usa", "italy", "poland", "india", "canada",
        "france", "hungary", "budapest", "washington", "new york",
    ]
    lowered = text.lower()
    return any(word in lowered for word in location_keywords) or "," in text


async def get_iso_country_from_text(text: str) -> Optional[str]:
    """
    Query Mapbox API to detect the country code from freeform text.
    """
    try:
        resp = await mapbox_api.async_search.mapbox(text)
        data = resp.body

        if not data.get("features"):
            return None

        for ctx in data["features"][0].get("context", []):
            if ctx.get("id", "").startswith("country"):
                return ctx.get("short_code", "").upper()
    except Exception as e:
        print(f"⚠️ Mapbox lookup failed for '{text[:40]}...': {e}")
    return None


async def extract_iso_country(obj: Any) -> Optional[str]:
    """
    Extract an ISO 3166-1 alpha-2 country code from a nested object.
    """
    # 1️⃣ Direct code
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and "country_code" in key.lower():
                return value.strip().upper()
            elif isinstance(value, (dict, list)):
                code = await extract_iso_country(value)
                if code:
                    return code

    # 2️⃣ Collect potential location strings
    text_values = extract_text_values(obj, skip_keys=[])
    for text in text_values:
        if looks_like_location(text):
            code = await get_iso_country_from_text(text)
            if code:
                return code

    return None
