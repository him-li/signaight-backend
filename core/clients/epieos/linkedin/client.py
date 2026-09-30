from core.rest_client import LongRedisCachedAPI

from .resources import LinkedinSearchResource, AsyncLinkedinSearchResource

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url="https://api.epieos.com/v1/search/email/",  # base api url
    params={},  # default params
    headers={"api-key": settings.EPIEOS_API_KEY},  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

# add users resource
api.add_resource(resource_name="search", resource_class=LinkedinSearchResource)
api.add_resource(resource_name="async_search", resource_class=AsyncLinkedinSearchResource)
