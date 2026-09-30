from core.rest_client import Resource, AsyncResource


class GeneralResourceMixin:
    actions = {
        "resolve_url": {"method": "GET",
                        "url": "url-resolver",
                        'params': {"url": {}}},
    }


class SearchResourceMixin:
    actions = {
        "users": {"method": "POST", "url": "search/users"},
        "filters": {"method": "POST", "url": "search/filters"},
    }


class ProfilesResourceMixin:
    actions = {
        "timeline": {"method": "GET", "url": "profiles/{}/timeline"},
        "header": {"method": "GET", "url": "profiles/{}/header"},
        "about": {"method": "GET",
                  "url": "profiles/{}/about",
                  'headers': {'x-version': 'update'}},
        "feed": {"method": "POST", "url": "profiles/{}/feed"},
        "likes": {"method": "POST", "url": "profiles/{}/likes"},
        "checkins": {"method": "POST", "url": "profiles/{}/checkins"},
        "uploaded_media": {"method": "POST",
                           "url": "profiles/{}/uploaded-media"},
        "friends": {"method": "POST", "url": "profiles/{}/friends"},
        "about_tabs_places_lived": {
            "method": "GET",
            "url": "profiles/{}/about-tabs?tab=PLACES_LIVED"},
        "pages_liked": {"method": "POST",
                        "url": "profiles/{}/likes"},
        "following": {"method": "POST",
                      "url": "profiles/{}/following"},
    }


class PostsResourceMixin:
    actions = {
        "post_node": {
            "method": "GET",
            "url": "posts/node",
            'params': {'transform': 'True', 'node_id': ''}},
        "media": {"method": "POST", "url": "posts/media/{}"},
    }


class PagesResourceMixin:
    actions = {
        # Path: pageId required
        "details": {"method": "GET", "url": "pages/{}/details"},
    }


class SearchResource(SearchResourceMixin, Resource):
    pass


class AsyncSearchResource(SearchResourceMixin, AsyncResource):
    pass


class ProfilesResource(ProfilesResourceMixin, Resource):
    pass


class AsyncProfilesResource(ProfilesResourceMixin, AsyncResource):
    pass


class GeneralResource(GeneralResourceMixin, Resource):
    pass


class AsyncGeneralResource(GeneralResourceMixin, AsyncResource):
    pass


class PostsResource(PostsResourceMixin, Resource):
    pass


class AsyncPostsResource(PostsResourceMixin, AsyncResource):
    pass


class PagesResource(PagesResourceMixin, Resource):
    pass


class AsyncPagesResource(PagesResourceMixin, AsyncResource):
    pass
