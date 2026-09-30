from core.rest_client import LongRedisCachedAPI

from .resources import (SearchResource, ProfilesResource, GeneralResource, PostsResource, PagesResource,
                        AsyncSearchResource, AsyncProfilesResource, AsyncGeneralResource, AsyncPostsResource, AsyncPagesResource)

from core.config import settings

# create api instance
api = LongRedisCachedAPI(
    api_root_url='https://api.vetric.io/facebook/v1/',  # base api url
    params={},  # default params
    headers={
        'x-api-key': settings.VETRIC_FACEBOOK_API_KEY,
        'x-version': 'update'
    },  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_statuses=[200, 201, 202, 204, 301, 308, 404],
)

# add users resource
api.add_resource(resource_name='search', resource_class=SearchResource)
api.add_resource(resource_name='async_search',
                 resource_class=AsyncSearchResource)
api.add_resource(resource_name='profiles', resource_class=ProfilesResource)
api.add_resource(resource_name='async_profiles',
                 resource_class=AsyncProfilesResource)
api.add_resource(resource_name='general', resource_class=GeneralResource)
api.add_resource(resource_name='async_general',
                 resource_class=AsyncGeneralResource)
api.add_resource(resource_name='pages', resource_class=PagesResource)
api.add_resource(resource_name='async_pages',
                 resource_class=AsyncPagesResource)
api.add_resource(resource_name='posts', resource_class=PostsResource)
api.add_resource(resource_name='async_posts',
                 resource_class=AsyncPostsResource)
