from core.rest_client import Resource, AsyncResource


class SearchResourceMixin:
    actions = {
        "submit": {"method": "POST", "url": "/api"},
        "get": {"method": "GET", "url": "/api"},
    }


class ActiveSearchResourceMixin:
    actions = {
        "submit": {"method": "POST",
                   "url": "/v1/linkedin/member/search/update"},
        "status": {"method": "GET",
                   "url": "/v1/linkedin/member/search/update"},
        "results": {"method": "GET",
                    "url": "/v1/linkedin/member/search/members"},
    }


class SearchResource(SearchResourceMixin, Resource):
    pass


class AsyncSearchResource(SearchResourceMixin, AsyncResource):
    pass


class ActiveSearchResource(ActiveSearchResourceMixin, Resource):
    pass


class AsyncActiveSearchResource(ActiveSearchResourceMixin, AsyncResource):
    pass
