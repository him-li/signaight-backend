from core.rest_client import LongRedisCachedAPI

from .resources import UserResource, AsyncUserResource

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    # base api url
    api_root_url="https://osint.rest/api/instagram/search_people",
    params={},  # default params
    # default headers
    headers={"Authorization": settings.SOCIAL_LINKS_API_KEY},
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

# add users resource
api.add_resource(resource_name="user", resource_class=UserResource)
api.add_resource(resource_name="async_user", resource_class=AsyncUserResource)
