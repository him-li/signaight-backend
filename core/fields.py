import asyncio
import re
import base64
import imghdr
import aioboto3
import mimetypes
import sys
import uuid
import os
from urllib.parse import urlparse, unquote
from cloudpathlib import S3Path as OriginS3Path
from io import BytesIO
import httpx
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import Any
from urllib.parse import urlparse

from core.utils.fetch_stream_follow_redirects import download_follow_redirects_streaming

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from core.logging import logger

from .storage import S3Client
from .config import settings

aioboto3_session = aioboto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)

EMAIL_WITH_STAR_REGEX_MASKED = re.compile(
    r"(^$)|(^[A-Za-z0-9.*_%+-]+@[A-Za-z0-9.*-]+\.[A-Za-z]{2,}$)"
)

class EmailStrMasked(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source, _handler):
        return core_schema.str_schema(
            pattern=EMAIL_WITH_STAR_REGEX_MASKED.pattern
        )


class S3Path(OriginS3Path):

    def as_url(self, presign: bool = False, expire_seconds: int = 86400) -> str:
        media_url = super().as_url(presign=presign, expire_seconds=expire_seconds)
        if not (_share_url := settings.AWS_SERVER_URL):
            return media_url
        try:
            media_url = urlparse(media_url)
            media_url = media_url._replace(scheme=_share_url.scheme)
            if _share_url.port is not None and _share_url.port not in [80, 443]:
                media_url = media_url._replace(
                    netloc=f"{_share_url.host}:{_share_url.port}"
                )
            else:
                media_url = media_url._replace(netloc=f"{_share_url.host}")
            if _share_url.path is not None:
                media_url = media_url._replace(
                    path=f"/{_share_url.path.strip('/')}{media_url.path}"
                )
        except Exception as e:
            logger.error(f"Unable to parse or modify presigned media url: {str(e)}")
        return f"{media_url.geturl()}"

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema["type"] = "string"
        json_schema["examples"] = [
            "s3://media.signaight.ai/profile_pictures/images/82.jpg",
            "https://media.signaight.ai/profile_pictures/images/82.jpg",
        ]
        json_schema["title"] = "S3Path"
        return json_schema

    @classmethod
    def validate(cls, v: str) -> Self:
        """Used as a Pydantic validator. See
        https://docs.pydantic.dev/2.0/usage/types/custom/"""
        return cls._profile_photos_to_storage(v)

    @classmethod
    def _validate(cls, value: Any) -> Self:
        """Used as a Pydantic validator. See
        https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types"""
        return cls._profile_photos_to_storage(value)

    @classmethod
    def _profile_photos_to_storage(cls, path: str) -> Self | None:
        client = S3Client.get_default_client()
        creds = client.sess.get_credentials()
        # TODO: rework this check for argument type
        if (
            isinstance(path, str)
            and ("http" in path or "https" in path)
            and (creds.access_key and creds.secret_key)
        ):
            path = path.strip(" '\"")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            }
            try:
                data, _, content_type = download_follow_redirects_streaming(
                    path, headers, logger
                )
                if data is None:
                    return None

                file_ext = None

                try:
                    if content_type:
                        file_ext = mimetypes.guess_extension(content_type, strict=True)
                except Exception as e:
                    logger.error(
                        f"Error guessing file extension from Content-Type: {str(e)}"
                    )

                if not file_ext:
                    try:
                        pathname = urlparse(path).path
                        path = unquote(pathname)
                        _, ext = os.path.splitext(path)
                        file_ext = ext if ext else None
                    except Exception as e:
                        logger.error(f"Error extracting file extension: {str(e)}")
                if file_ext:

                    file_key = str(uuid.uuid4())
                    file_path = "profile_photos/{}/{}/{}/{}{}".format(
                        file_key[0:1], file_key[1:3], file_key[3:8], file_key, file_ext
                    )

                    path = cls(f"s3://{client.bucket}/{file_path}")

                    buffer = BytesIO(data)
                    buffer.seek(0)  # rewind for reading later
                    try:
                        asyncio.create_task(
                            async_save_image_to_s3(client.bucket, file_path, buffer)
                        )
                    except Exception as e:
                        logger.error(
                            f"There is no possible to use async"
                            " loop for now, fallback to sync upload."
                            f" Error: {str(e)}."
                        )
                        path.write_bytes(buffer)
            except httpx.TooManyRedirects as e:
                logger.warning(f"Unexpected error. Too many redirects: {str(e)}")
                return None
            except httpx.HTTPError as e:
                logger.error(f"HTTP error: {str(e)} address: {path}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error. {str(e)}")
                return None
        elif isinstance(path, str) and (
            path.strip().startswith("data:image/") or path.strip().startswith("/9j")
        ):
            try:
                path = cls._save_base64_image_to_s3(client, path)
            except Exception as e:
                logger.error(f"Failed to handle base64 image: {e}")
                path = None
        elif isinstance(path, str) and path.startswith("s3://"):
            path = cls(path)
        elif isinstance(path, S3Path):
            return path
        else:
            path = None
        return path

    @classmethod
    def _save_base64_image_to_s3(cls, client, input_data: str) -> Self | None:
        match = re.match(r"data:(image/\w+);base64,(.+)", input_data)

        mime_type: str | None = None
        image_bytes: bytes | None = None

        if match:
            mime_type, b64_payload = match.groups()
            try:
                image_bytes = base64.b64decode(b64_payload)
            except Exception as e:
                logger.error(f"Error decoding base64 data URL: {str(e)}")
                return None
        elif _is_probably_base64(input_data):
            try:
                image_bytes = _b64decode_relaxed(input_data)
            except Exception as e:
                logger.error(f"Error decoding raw base64: {str(e)}")
                return None

        file_ext: str
        if mime_type:
            file_ext = mimetypes.guess_extension(mime_type, strict=True) or ".jpg"
        else:
            # Guess from bytes
            file_ext = _guess_ext_from_bytes(image_bytes, fallback_ext=".jpg")

        file_key = str(uuid.uuid4())
        file_path = f"profile_photos/{file_key[0]}/{file_key[1:3]}/{file_key[3:8]}/{file_key}{file_ext}"

        s3_path = cls(f"s3://{client.bucket}/{file_path}")

        buffer = BytesIO(image_bytes)
        buffer.seek(0)

        try:
            asyncio.create_task(async_save_image_to_s3(
                client.bucket, file_path, buffer))
        except Exception as e:
            logger.error(
                f"Async not available, fallback to sync upload. Error: {str(e)}")
            s3_path.write_bytes(buffer)
        return s3_path


async def async_save_image_to_s3(bucket: str, path: str, data: BytesIO):
    async with aioboto3_session.client("s3") as s3:
        try:
            await s3.upload_fileobj(data, bucket, path)
        except Exception as e:
            print(f"Unable to s3 upload data to {bucket}/{path}: " f"{str(e)} ({type(e)})")


def s3path_serializer(v: S3Path | str | None, info=None):
    try:
        if not info:
            return str(v)
        if isinstance(v, str):
            v = S3Path(v)
        if isinstance(v, S3Path):
            return (
                v.as_url(
                    presign=True, expire_seconds=settings.AWS_S3_PRESIGNED_LINKS_TTL
                )
                if info.mode == "json"
                else str(v)
            )
    except Exception as e:
        print("s3path_serializer failed for value:", str(e))
        return None
    return v

def _is_probably_base64(s: str) -> bool:
    # Heuristic: only base64 charset + possible padding, and length mod 4 in {0,2,3} (padding can be missing)
    s_stripped = re.sub(r"\s+", "", s)
    return bool(re.match(r"^[A-Za-z0-9+/]+={0,2}$", s_stripped)) and len(s_stripped) >= 16

def _b64decode_relaxed(s: str) -> bytes:
    s = re.sub(r"\s+", "", s)
    # Add missing padding if necessary
    missing = (-len(s)) % 4
    if missing:
        s += "=" * missing
    return base64.b64decode(s)

def _guess_ext_from_bytes(b: bytes, fallback_ext: str = ".jpg") -> str:
    kind = imghdr.what(None, h=b)  # 'jpeg', 'png', 'gif', 'webp', etc.
    if kind == "jpeg":
        return ".jpg"
    if kind:
        return f".{kind}"
    return fallback_ext
