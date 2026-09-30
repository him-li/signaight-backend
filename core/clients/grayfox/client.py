from core.rest_client import LongRedisCachedAPI

from .resources import (SearchResource, AsyncSearchResource,
                        ActiveSearchResource, AsyncActiveSearchResource)

from core.config import settings


# create api instance
api = LongRedisCachedAPI(
    api_root_url='https://eye-6adaad69fa3d.profileintel.com',  # base api url
    params={},  # default params
    headers={
        'x-api-key': settings.GRAYFOX_API_KEY
    },  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_default_ttl=864000000000 # default cache ttl in seconds for 100 days
)

# add users resource
api.add_resource(resource_name='search', resource_class=SearchResource)
api.add_resource(resource_name='async_search',
                 resource_class=AsyncSearchResource)


active_search_api = LongRedisCachedAPI(
    api_root_url='https://dolphin-social-api-50a982bb.profileintel.com',
    params={
        "access_token": settings.GRAYFOX_API_KEY,
        "max_results": 100,
        "max_page_size": 100
    },  # default params
    headers={},  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_default_ttl=864000000000 # default cache ttl in seconds for 100 days
)

active_search_api.add_resource(
    resource_name='active_search', resource_class=ActiveSearchResource)
active_search_api.add_resource(resource_name='async_active_search',
                               resource_class=AsyncActiveSearchResource)
