from core.rest_client import Resource, AsyncResource


class ServiceLogsResourceMixin:
    actions = {
        "post": {"method": "POST",
                 "url": "api/v1/service-logs"},
        "list": {"method": "GET",
                 "url": "api/v1/service-logs"},
        "get": {"method": "GET",
                "url": "api/v1/service-logs/{}"},
    }


class ServiceLogsResource(ServiceLogsResourceMixin, Resource):
    pass


class AsyncServiceLogsResource(ServiceLogsResourceMixin, AsyncResource):
    pass
