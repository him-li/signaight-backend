from core.rest_client import Resource, AsyncResource


class LinkedinSearchResourceMixin:
    actions = {
        # Params: query required
        "lookup_by_email_v2": {
            "method": "GET",
            "url": "lookup_by_email/v2",
            "params": {},
        },
        "email_to_profile": {"method": "GET",
                             "url": "email_to_profile",
                             "params": {}},
        "search_people_new": {
            "method": "GET",
            "url": "search_people_new",
            "params": {},
        },
    }


class LinkedinSearchResource(LinkedinSearchResourceMixin, Resource):
    pass


class AsyncLinkedinSearchResource(LinkedinSearchResourceMixin, AsyncResource):
    pass
