from core.rest_client import LongRedisCachedAPI

from .resources import (UserResource, GeneralResource,
                        AsyncUserResource, AsyncGeneralResource)

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url='https://api.vetric.io/instagram/v1/',  # base api url
    params={},  # default params
    headers={
        'x-api-key': settings.VETRIC_INSTAGRAM_API_KEY,
        'x-version': '2026-1'
    },  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_default_ttl=172800  # use a 2-day cache to stabilize short-lived photo URLs
)

# add users resource
api.add_resource(resource_name='user', resource_class=UserResource)
api.add_resource(resource_name='async_user', resource_class=AsyncUserResource)
api.add_resource(resource_name='general', resource_class=GeneralResource)
api.add_resource(resource_name='async_general',
                 resource_class=AsyncGeneralResource)
