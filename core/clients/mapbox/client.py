from core.rest_client import LongRedisCachedAPI
from core.config import settings

from .resources import MapboxResource, AsyncMapboxResource

# create api instance
api = LongRedisCachedAPI(
    api_root_url='https://api.mapbox.com/geocoding/v5/mapbox.places/',
    params={"access_token": settings.NEXT_PUBLIC_MAPBOX_TOKEN},
    headers={},  # default headers
    timeout=100,  # default timeout in seconds
    append_slash=False,  # append slash to final url
    json_encode_body=True,  # encode body as json
    cache_default_ttl=864000000000 # default cache ttl in seconds for 100 days
)

# add users resource
api.add_resource(resource_name='search', resource_class=MapboxResource)
api.add_resource(resource_name='async_search', resource_class=AsyncMapboxResource)
