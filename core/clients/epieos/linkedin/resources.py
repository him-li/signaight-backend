from core.rest_client import Resource, AsyncResource


class LinkedinSearchResourceMixin:
    actions = {
        # Params: query required
        "osinter": {
            "method": "POST",
            "url": "osinter",
        },
    }
    

class LinkedinSearchResource(LinkedinSearchResourceMixin, Resource):
    pass


class AsyncLinkedinSearchResource(LinkedinSearchResourceMixin, AsyncResource):
    pass
