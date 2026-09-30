from core.rest_client import LongRedisCachedAPI

from .resources import (TwitterSearch, TwitterProfile,
                        AsyncTwitterSearch, AsyncTwitterProfile)

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url="https://api.vetric.io/twitter/v1",  # base api url
    params={},  # default params
    # default headers
    headers={"x-api-key": settings.VETRIC_TWITTER_API_KEY},
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

# add users resource
api.add_resource(resource_name="search", resource_class=TwitterSearch)
api.add_resource(resource_name="async_search", resource_class=AsyncTwitterSearch)
api.add_resource(resource_name="profile", resource_class=TwitterProfile)
api.add_resource(resource_name="async_profile", resource_class=AsyncTwitterProfile)
