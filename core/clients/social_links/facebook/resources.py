from core.rest_client import Resource, AsyncResource


class SearchResourceMixin:
    actions = {
        "users": {"method": "GET", "url": "", "params": {}},
    }


class SearchResource(SearchResourceMixin, Resource):
    pass


class AsyncSearchResource(SearchResourceMixin, AsyncResource):
    pass
