import httpcore
import logging
from typing import Optional, Union

cache_namespace = 'external-apis-cache'
logger = logging.getLogger(__name__)

def normalized_url(url: Union[httpcore.URL, str, bytes]) -> str:
    if isinstance(url, str):  # pragma: no cover
        return url

    if isinstance(url, bytes):  # pragma: no cover
        return url.decode("ascii")

    if isinstance(url, httpcore.URL):
        port = f":{url.port}" if url.port is not None else ""
        return f'{url.scheme.decode("ascii")}://{url.host.decode("ascii")}{port}{url.target.decode("ascii")}'
    assert False, "Invalid type for `normalized_url`"  # pragma: no cover

def get_advanced_cache_key(
    request: httpcore.Request,
    body_hash: Optional[str] = None
) -> str:
    request_method = request.method.decode("ascii")
    encoded_url = normalized_url(request.url)
    key = f"{cache_namespace}:{request_method}:{encoded_url}"
    # if request_method in ('POST', 'PUT', 'PATCH'):
    key = "{}:{}".format(key, body_hash)
    return key
