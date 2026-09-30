from core.rest_client import Resource, AsyncResource


class DsResourceMixin:
    actions = {
        "government_experience": {"method": "POST",
                                  "url": "posts/government_experience"},
        "anti_israel": {"method": "POST",
                                  "url": "posts/anti_israel"},
        "anti_usa": {"method": "POST",
                     "url": "posts/anti_usa"},
        "flexibility_skills": {"method": "POST",
                               "url": "posts/flexibility_skills"},
        "flexibility_work": {"method": "POST",
                             "url": "posts/flexibility_work"},
        "sociable_events": {"method": "POST",
                            "url": "posts/sociable_events"},
        "altruism_post": {"method": "POST",
                          "url": "posts/altruism_post"},
        "altruism_page": {"method": "POST",
                          "url": "posts/altruism_page"},
        "sentiment_analysis": {"method": "POST",
                               "url": "posts/sentiment-analysis"},
        "work_under_pressure": {"method": "POST",
                                "url": "posts/work_under_pressure"},
        "extreme_sports": {"method": "POST",
                           "url": "posts/extreme_sports"},
        "support_israel": {"method": "POST",
                           "url": "posts/support_israel"},
        "curiosity_international_travels": {
            "method": "POST",
            "url": "posts/curiosity_international_travels"},
        "search_engine_matching":  {
            "method": "POST",
            "url": "posts/search_engine_matching"
        },
        "courage_international_travels": {
            "method": "POST",
            "url": "posts/courage_international_travels"},
        "team_work_experience": {
            "method": "POST",
            "url": "posts/team_work_experience"},
        "flexibility_skill_set": {
            "method": "POST",
            "url": "posts/flexibility_skill_set"},
        "flexibility_transition_industries": {
            "method": "POST",
            "url": "posts/flexibility_transition_industries"},
        "filter_candidates": {
            "method": "POST",
            "url": "posts/filter_candidates"},
        "match_candidates": {
            "method": "POST",
            "url": "posts/match_candidates"},
        "team_related_activities": {
            "method": "POST",
            "url": "posts/team_related_activities"},
        "volunteering_experience": {
            "method": "POST",
            "url": "posts/volunteering_experience"},
        "foodie_intro": {
            "method": "POST",
            "url": "posts/foodie_intro"},
        "foodie_pages": {
            "method": "POST",
            "url": "posts/foodie_pages"},
        "curiosity_tuned_score": {
            "method": "POST",
            "url": "posts/curiosity_tuned_score"},
        "resilience_tuned_score": {
            "method": "POST",
            "url": "posts/resilience_tuned_score"},
        "common_name": {
            "method": "POST",
            "url": "posts/is_common_name"
        },
        "extremism": {
            "method": "POST",
            "url": "posts/is_extrimism"},
        "check_weapons": {
            "method": "POST",
            "url": "posts/check_weapons"
        },
        "name_resolution": {
            "method": "POST",
            "url": "posts/name_resolution"
        },
    }


class DsResource(DsResourceMixin, Resource):
    pass


class AsyncDsResource(DsResourceMixin, AsyncResource):
    pass
