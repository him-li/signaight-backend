from core.rest_client import Resource, AsyncResource


class MapboxResourceMixin:
    actions = {
        "mapbox": {"method": "GET", "url": "{}.json"},
    }


class MapboxResource(MapboxResourceMixin, Resource):
    pass


class AsyncMapboxResource(MapboxResourceMixin, AsyncResource):
    pass
