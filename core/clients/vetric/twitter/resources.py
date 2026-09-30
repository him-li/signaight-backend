from core.rest_client import Resource, AsyncResource


class TwitterSearchMixin:
    actions = {
        "people": {"method": "GET", "url": "/search/people", "params": {}},
    }


class TwitterProfileMixin:
    actions = {
        "profile_details_by_screen_name": {"method": "GET",
                                           "url": "/profile/{}/details"},
        "profile_tweets_by_id": {"method": "GET",
                                           "url": "/profile/{}/tweets"},
    }


class TwitterSearch(TwitterSearchMixin, Resource):
    pass


class AsyncTwitterSearch(TwitterSearchMixin, AsyncResource):
    pass


class TwitterProfile(TwitterProfileMixin, Resource):
    pass


class AsyncTwitterProfile(TwitterProfileMixin, AsyncResource):
    pass
