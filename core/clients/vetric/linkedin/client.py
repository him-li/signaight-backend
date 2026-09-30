from core.rest_client import LongRedisCachedAPI

from .resources import (LinkedinSearch, LinkedinProfile, LinkedinCompany, LinkedinPosts,
                        AsyncLinkedinSearch, AsyncLinkedinProfile, AsyncLinkedinCompany, AsyncLinkedinPosts)

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url="https://api.vetric.io/linkedin/v1",  # base api url
    params={},  # default params
    # default headers
    headers={"x-api-key": settings.VETRIC_LINKEDIN_API_KEY},
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
)

# add users resource
api.add_resource(resource_name="search", resource_class=LinkedinSearch)
api.add_resource(resource_name="async_search",
                 resource_class=AsyncLinkedinSearch)
api.add_resource(resource_name="profile", resource_class=LinkedinProfile)
api.add_resource(resource_name="async_profile",
                 resource_class=AsyncLinkedinProfile)
api.add_resource(resource_name="company", resource_class=LinkedinCompany)
api.add_resource(resource_name="async_company", resource_class=AsyncLinkedinCompany)
api.add_resource(resource_name="posts", resource_class=LinkedinPosts)
api.add_resource(resource_name="async_posts", resource_class=AsyncLinkedinPosts)

