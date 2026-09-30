import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_TEXT

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (update_evaluation_factors,
                                     build_post_text_list,
                                     build_post_photo_text_list,
                                     build_fb_pages_photo_text_list)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class MoralValuesActions(PersonBaseActions):

    @rule_action()
    def set_volunteering_experience(self):
        factor = {
            "title": ("{} volunteering experience").format(
                self.get_person_name()),
            "score": 0
        }
        try:
            volunteering_experiences = (self.person.biographic_details.work.
                                        linkedin_work.volunteering_experiences)
            if len(volunteering_experiences) > 0:
                factor["score"] = 6
            total_duration = 0
            for item in volunteering_experiences:
                if item.duration:
                    duration_years = (item.duration.years if
                                      item.duration.years else 0)
                    duration_months = (item.duration.months if
                                       item.duration.months else 0)
                    duration = duration_years * 12 + duration_months
                elif item.start_month_year:
                    start_date = pendulum.parse(str(item.start_month_year),
                                                strict=False)
                    if item.end_month_year:
                        end_date = pendulum.parse(str(item.end_month_year),
                                                  strict=False)
                    else:
                        end_date = pendulum.today()
                    duration = end_date.diff(start_date).in_months()
                total_duration += duration

            if total_duration >= 6:
                factor['score'] += 1
            if len(volunteering_experiences) == 2:
                factor['score'] += 1
            if len(volunteering_experiences) >= 3:
                factor['score'] += 2

            factor["title"] = (
                "{person} has volunteering experience.").format(
                    person=self.get_person_name(),)
        except AttributeError:
            volunteering_experiences = []
        if not isinstance(volunteering_experiences, list):
            return
        self.evaluation.moral_values = update_evaluation_factors(
            self.evaluation.moral_values, factor)

    @rule_action()
    def set_person_altruism(self):
        score = 0

        if posts := self.person.posts:
            posts_list = build_post_text_list(posts)
            logger.debug('Rules engine: MoralValuesActions'
                         ' altruism_post in posts')
            try:
                ds_response = ds_app_api.ds_request.altruism_post(
                    body=posts_list,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                posts_res = ds_response.body
            except Exception:
                posts_res = {}
            posts_altruism_count = 0
            if posts_res:
                for res in posts_res:
                    if res.get("is_altruism"):
                        posts_altruism_count += 1
                if posts_altruism_count > 0 and posts_altruism_count < 2:
                    score += 1
                elif posts_altruism_count >= 2:
                    score += 2

        if interests := self.person.interests:
            page_names_list = []
            if interests.pages:
                page_names_list = [
                    {"hash": page.fb_page_name, "text": page.fb_page_name}
                    for page in interests.pages]
            logger.debug('Rules engine: MoralValuesActions'
                         ' altruism_page in interests')
            try:
                ds_response = ds_app_api.ds_request.altruism_page(
                    body=page_names_list,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                pages_res = ds_response.body
            except Exception:
                pages_res = {}
            pages_altruism_count = 0
            if pages_res:
                for res in pages_res:
                    if res.get("is_altruism"):
                        pages_altruism_count += 1
                if pages_altruism_count > 0 and pages_altruism_count < 3:
                    score += 0.5
                elif pages_altruism_count >= 3:
                    score += 1

        if score:
            score = score + 7

            if score > 10:
                score = min(score, 10)

            factor = {
                "title": ("{}'s altruism").format(
                    self.get_person_name()),
                "score": score
            }
            self.evaluation.moral_values = update_evaluation_factors(
                self.evaluation.moral_values, factor)

    @rule_action(
        params={"country": FIELD_TEXT}
    )
    def set_person_supporting_country(self, country):
        if country == 'IL':
            score = 0
            if posts := self.person.posts:
                posts_list = build_post_photo_text_list(posts)
                try:
                    ds_response = ds_app_api.ds_request.support_israel(
                        body=posts_list["posts_list"],
                        headers={"x-remote-context": build_person_urn(self.person.id)},
                    )
                    posts_res = ds_response.body
                except Exception:
                    posts_res = {}
                posts_supporting_israel_count = 0
                if posts_res:
                    for res in posts_res:
                        if res.get("is_support_israel"):
                            posts_supporting_israel_count += 1
                    if (posts_supporting_israel_count > 0 and
                            posts_supporting_israel_count <= 2):
                        score += 6
                    elif posts_supporting_israel_count == 3:
                        score += 7
                    elif posts_supporting_israel_count >= 4:
                        score += 8

            if interests := self.person.interests:
                page_names_list = build_fb_pages_photo_text_list(
                    interests.pages)
                try:
                    ds_response = ds_app_api.ds_request.support_israel(
                        body=page_names_list,
                        headers={
                            'x-remote-context': build_person_urn(self.person.id)
                        }
                    )
                    pages_res = ds_response.body
                except Exception:
                    pages_res = {}
                pages_supporting_israel_count = 0
                if pages_res:
                    for res in pages_res:
                        if res.get("is_support_israel"):
                            pages_supporting_israel_count += 1
                    if pages_supporting_israel_count:
                        if score < 6:
                            score = 6
                        score += pages_supporting_israel_count * 0.5

            if score > 10:
                score = min(score, 10)

            if score:
                factor = {
                    "title": ("{} supports Israel").format(
                        self.get_person_name()),
                    "score": score
                }
                self.evaluation.moral_values = update_evaluation_factors(
                    self.evaluation.moral_values, factor)
