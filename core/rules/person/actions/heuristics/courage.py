from business_rules.actions import rule_action

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (
    update_evaluation_factors,
    build_post_photo_list)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class CourageActions(PersonBaseActions):

    @rule_action()
    def set_person_travel_risky_areas_check_ins(
        self,
    ):
        check_ins = None
        try:
            check_ins = (self.person.personal_details.location.
                         check_ins.fb_check_ins)
        except Exception:
            pass
        posts = self.person.posts
        europe_namerica_risky_checkins = 0
        asia_samerica_camerica_risky_checkins = 0
        africa_risky_checkins = 0
        continents = []
        countries = []
        if check_ins:
            try:
                check_ins_list = [check_in.model_dump()
                                  for check_in in check_ins]
                check_ins_req = {'hash': str(
                    check_ins_list), 'checkins': check_ins_list}
                (europe_namerica_risky_checkins,
                 asia_samerica_camerica_risky_checkins,
                 africa_risky_checkins) = process_check_ins(
                    build_person_urn(self.person.id),
                    check_ins_req,
                    europe_namerica_risky_checkins,
                    asia_samerica_camerica_risky_checkins,
                    africa_risky_checkins,
                    continents,
                    countries,
                )
            except Exception as e:
                logger.info(str(e))

        if posts:
            try:
                posts_list = [
                    {'title': (post.instagram_post_location.
                               instagram_location_name)}
                    for post in posts if post.instagram_post_location]
                posts_req = {'hash': str(
                    posts_list), 'checkins': posts_list}
                (europe_namerica_risky_checkins,
                 asia_samerica_camerica_risky_checkins,
                 africa_risky_checkins) = process_check_ins(
                    build_person_urn(self.person.id),
                    posts_req,
                    europe_namerica_risky_checkins,
                    asia_samerica_camerica_risky_checkins,
                    africa_risky_checkins,
                    continents,
                    countries,
                )
            except Exception as e:
                logger.info(str(e))

        score = 0
        if (europe_namerica_risky_checkins or
                asia_samerica_camerica_risky_checkins or
                africa_risky_checkins):
            score = 5
            if europe_namerica_risky_checkins >= 3:
                score += 1
            elif europe_namerica_risky_checkins >= 1:
                score += 0.5

            if asia_samerica_camerica_risky_checkins >= 3:
                score += 2.5
            elif asia_samerica_camerica_risky_checkins == 2:
                score += 2
            elif asia_samerica_camerica_risky_checkins == 1:
                score += 1.5

            if africa_risky_checkins >= 2:
                score += 3
            elif africa_risky_checkins == 1:
                score += 2.5

            if len(countries) >= 3:
                score += 1
            if len(continents) > 1:
                score += 2

        if score:

            if score > 10:
                score = 10

            factor = {
                "title": "{} has travel check_ins in risky areas".format(
                    self.get_person_name()),
                "score": score,
            }
            self.evaluation.courage = (
                update_evaluation_factors(
                    self.evaluation.courage, factor))

    @rule_action()
    def set_person_extreme_sports(self):
        posts = self.person.posts
        if posts:
            photo_list = build_post_photo_list(posts)
            try:
                logger.debug('Rules engine: CourageActions'
                             ' extreme_sports in posts')
                ds_response = ds_app_api.ds_request.extreme_sports(
                    body=photo_list,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                extreme_sports_list = ds_response.body
                posts_count = len(photo_list)
                extreme_count = sum(
                    1 for photo in extreme_sports_list if
                    photo.get("is_extreme_sport"))
                if posts_count:
                    extreme_percentage = extreme_count / posts_count
                else:
                    extreme_percentage = 0
                score = 0
                if extreme_percentage > 0 and extreme_percentage < 0.1:
                    score = 3
                if extreme_percentage >= 0.1 and extreme_percentage < 0.2:
                    score = 7
                if extreme_percentage >= 0.2 and extreme_percentage < 0.3:
                    score = 9
                if extreme_percentage >= 0.3:
                    score = 10
                if score:
                    factor = {
                        "title": ("{} has extreme sports detected").format(
                            self.get_person_name()),
                        "score": score,
                    }
                    self.evaluation.courage = (
                        update_evaluation_factors(
                            self.evaluation.courage, factor))

            except Exception as e:
                logger.info(str(e))


def process_check_ins(context,
                      check_ins_req,
                      europe_namerica_risky_checkins,
                      asia_samerica_camerica_risky_checkins,
                      africa_risky_checkins,
                      continents,
                      countries):
    courage_res = ds_app_api.ds_request.courage_international_travels(
        body=check_ins_req,
        headers={'x-remote-context': context}
    )
    courage_res_body = courage_res.body
    for checkin in courage_res_body.get("checkins"):
        if checkin.get("is_courageous"):
            if region := checkin.get("region"):
                if isinstance(region, str):
                    if region.lower() in ['europe', 'north america']:
                        europe_namerica_risky_checkins += 1
                    if region.lower() in ['asia', 'south america',
                                          'central america']:
                        asia_samerica_camerica_risky_checkins += 1
                    if region.lower() in ['africa']:
                        africa_risky_checkins += 1
                    if region.lower() not in continents:
                        continents.append(region)
            if country := checkin.get("country"):
                if isinstance(region, str):
                    if country.lower() not in countries:
                        countries.append(country)

    return (europe_namerica_risky_checkins,
            asia_samerica_camerica_risky_checkins, africa_risky_checkins)
