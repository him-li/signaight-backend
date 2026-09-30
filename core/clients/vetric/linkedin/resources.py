from core.rest_client import Resource, AsyncResource


class LinkedinSearchMixin:
    actions = {
        "people": {"method": "GET", "url": "/search/people", "params": {}},
        "companies": {"method": "GET", "url": "/search/companies",
                      "params": {}},
    }


class LinkedinProfileMixin:
    actions = {
        "resolve_url": {"method": "GET", "url": "/url-resolver", "params": {}},
        "overview": {"method": "GET", "url": "/profile/{}/overview"},
        "about": {"method": "GET", "url": "/profile/{}/about"},
        "experience": {"method": "GET", "url": "/profile/{}/experience"},
        "skills": {"method": "GET", "url": "/profile/{}/skills"},
        "education": {"method": "GET", "url": "/profile/{}/education"},
        "recommendations_received": {
            "method": "GET",
            "url": "/profile/{}/recommendations?type=received"},
        "contact_info": {"method": "GET", "url": "/profile/{}/contact-info"},
        # NOTE: it is possible to use 3 different types, just this is mapped
        "activity_posts": {"method": "GET",
                           "url": "/profile/{}/activity?type=posts"},
        "activity_reactions": {"method": "GET",
                               "url": "/profile/{}/activity?type=reactions"},
        # NOTE: it is possible to use 5 different types, just this is mapped
        "interests_influencers": {"method": "GET",
                                  "url": "/profile/{}/interests?type=influencers"},  # noqa
        "courses": {"method": "GET", "url": "/profile/{}/courses"},
        "events": {"method": "GET", "url": "/profile/{}/events"},
        "honors_awards": {"method": "GET",
                          "url": "/profile/{}/honors-and-awards"},
        "languages": {"method": "GET", "url": "/profile/{}/languages"},
        "licences_certifications": {
            "method": "GET",
            "url": "/profile/{}/licenses-and-certifications"},
        "organizations": {"method": "GET", "url": "/profile/{}/organizations"},
        "volunteering": {"method": "GET",
                         "url": "/profile/{}/volunteering-experience"},
        "projects": {"method": "GET", "url": "/profile/{}/projects"},
        "publications": {"method": "GET", "url": "/profile/{}/publications"},
        "test_scores": {"method": "GET", "url": "/profile/{}/test-scores"},
    }


class LinkedinCompanyMixin:
    actions = {
        "details": {"method": "GET", "url": "company/{}/details"},
    }

class LinkedinPostsMixin:
    actions = {
        "info": {"method": "GET", "url": "post/{}/info"},
    }


class LinkedinSearch(LinkedinSearchMixin, Resource):
    pass


class AsyncLinkedinSearch(LinkedinSearchMixin, AsyncResource):
    pass


class LinkedinProfile(LinkedinProfileMixin, Resource):
    pass


class AsyncLinkedinProfile(LinkedinProfileMixin, AsyncResource):
    pass


class LinkedinCompany(LinkedinCompanyMixin, Resource):
    pass


class AsyncLinkedinCompany(LinkedinCompanyMixin, AsyncResource):
    pass

class LinkedinPosts(LinkedinPostsMixin, Resource):
    pass

class AsyncLinkedinPosts(LinkedinPostsMixin, AsyncResource):
    pass
