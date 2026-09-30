from core.rest_client import Resource, AsyncResource


class UserResourceMixin:
    actions = {
        # Params: query required
        "search": {"method": "GET", "url": "", "params": {}},
    }


class UserResource(UserResourceMixin, Resource):
    pass


class AsyncUserResource(UserResourceMixin, AsyncResource):
    pass
