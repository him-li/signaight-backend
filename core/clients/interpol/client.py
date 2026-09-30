from core.rest_client import API
from core.config import settings

from .resources import SearchResource, AsyncSearchResource

# create api instance
api = API(
    api_root_url="https://ws-public.interpol.int/notices/v1/",
    params={},
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Cache-control": "no-cache",
        "Cookie": "",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.interpol.int",
        "Referer": "https://www.interpol.int/",
        "Connection": "keep-alive",
    },  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

# add users resource
api.add_resource(resource_name="search", resource_class=SearchResource)
api.add_resource(resource_name="async_search", resource_class=AsyncSearchResource)
