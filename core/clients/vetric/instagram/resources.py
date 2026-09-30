from core.rest_client import Resource, AsyncResource


class UserResourceMixin:
    actions = {
        # Path: userId required
        'info': {'method': 'GET', 'url': '/users/{}/info'},
        # Path: username required
        'usernameinfo': {'method': 'GET', 'url': '/users/{}/usernameinfo'},
        # Params: q required
        'search': {'method': 'GET', 'url': '/users/search'},
        # Path: usedId, Params: rank_token. Both required
        'following':  {'method': 'GET',
                       'url': '/friendships/{}/following',
                       'params': {'rank_token': {}}},
        'followers':  {'method': 'GET',
                       'url': '/friendships/{}/followers',
                       'params': {'cursor': {}},
                       'headers': {"x-version": "2026-1"}},
        # Path: usedId
        'feed':   {'method': 'GET', 'url': '/feed/user/{}'},
    }


class GeneralResourceMixin:
    actions = {
        'resolve_url': {'method': 'GET', 'url': '/url-resolver', 'params': {}}
    }


class UserResource(UserResourceMixin, Resource):
    pass


class AsyncUserResource(UserResourceMixin, AsyncResource):
    pass


class GeneralResource(GeneralResourceMixin, Resource):
    pass


class AsyncGeneralResource(GeneralResourceMixin, AsyncResource):
    pass
