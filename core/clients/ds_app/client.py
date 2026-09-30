from core.rest_client import LongRedisCachedAPI

from .resources import DsResource, AsyncDsResource

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url=settings.DS_APPS_BASE_URL,  # base api url
    params={},  # default params
    headers={
        'Authorization': f"Bearer {settings.DS_APPS_API_KEY}"
    },  # default headers
    timeout=500,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_default_ttl=864000000000  # default cache ttl in seconds for 100 days
)

# add users resource
api.add_resource(resource_name='ds_request', resource_class=DsResource)
api.add_resource(resource_name='async_ds_request',
                 resource_class=AsyncDsResource)
