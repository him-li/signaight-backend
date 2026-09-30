from core.rest_client import Resource, AsyncResource


class SearchResourceMixin:
    actions = {
        "search": {"method": "GET", "url": "/red"},
        "enrich" : {"method": "GET", "url": "/red/{}"},
        "images" : {"method": "GET", "url": "/red/{}/images"}
    }


class SearchResource(SearchResourceMixin, Resource):
    pass


class AsyncSearchResource(SearchResourceMixin, AsyncResource):
    pass
