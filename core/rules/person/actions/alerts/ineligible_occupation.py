import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_NUMERIC, FIELD_SELECT

from core.rules.person.utils import (update_heuristics_score,
                                     check_min_experience,
                                     create_position_model_list_unique,
                                     create_position_model_list_additive)
from core.clients.ds_app import api as ds_app_api
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class IneligibleOccupationActions(PersonBaseActions):

    @rule_action(params={
        "min_months": FIELD_NUMERIC,
        "min_intermidate_months": FIELD_NUMERIC
    })
    def set_person_without_minimun_experience(self,
                                              min_months,
                                              min_intermidate_months):
        positions = create_position_model_list_unique(self.person)
        if not positions:
            return
        positions.sort(key=lambda position: position.period.date_from)
        positions.reverse()
        experience_months = check_min_experience(positions)
        heuristic = {
            "title": ("Lack of Work Experience"),
            "description": ("{person} has less than {min_months} months of "
                            "experience").format(
                                person=self.get_person_name(),
                                min_months=min_months),
            "score": 8
        }
        if experience_months < min_intermidate_months:
            heuristic['score'] = 10
        self.alerts.ineligible_occupation = update_heuristics_score(
            self.alerts.ineligible_occupation, heuristic)

    @rule_action(params={
        "titles": FIELD_SELECT
    })
    def set_person_with_journalism_background(self, titles):
        heuristic = {
            "title": ("Journalism Background"),
            "description": ("{} has journalism background").format(
                self.get_person_name()),
            "score": 10
        }
        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return
            positions.sort(key=lambda position: position.period.date_from)
        except Exception:
            return
        last_title_date = None
        for position in positions:
            for title in titles:
                if title in position.title.lower():
                    last_title_date = (position.period.date_to if
                                       position.period.date_to and
                                       position.period.date_to != "Present"
                                       else pendulum.now().to_date_string())

        positions.reverse()
        now = pendulum.now()
        if (now - pendulum.parse(last_title_date)).in_months() > 36 and (
                now - pendulum.parse(last_title_date)).in_months() < 60:
            heuristic['score'] -= 3
        if (now - pendulum.parse(last_title_date)).in_months() >= 60:
            heuristic['score'] -= 5

        self.alerts.ineligible_occupation = update_heuristics_score(
            self.alerts.ineligible_occupation, heuristic)

    @rule_action()
    def set_person_with_government_background(self):
        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return
        except Exception:
            return
        last_field_date = None
        work_experience = {
            "hash": str(positions),
            "work_experience": [position.model_dump() for position in
                                positions]
        }
        logger.debug('Rules engine: IneligibleOccupationActions'
                     ' government_experience for work experience')
        try:
            ds_response = ds_app_api.ds_request.government_experience(
                body=work_experience,
                headers={'x-remote-context': build_person_urn(self.person.id)}
            )
            ds_response_body = ds_response.body
        except Exception as e:
            ds_response = {}
            logger.info(str(e))
        if ds_response:
            if government_experience := ds_response_body.get(
                    "government_experience"):
                for i, position in enumerate(government_experience):
                    if position.get("has_government_experience"):
                        position = positions[i]
                        try:
                            last_field_date = (
                                position.period.date_to if
                                position.period.date_to and
                                position.period.date_to != "Present"
                                else pendulum.now().to_date_string())
                            break

                        except Exception as e:
                            print(e)
                            continue
        if last_field_date:
            heuristic = {
                "title": ("National security agency, "
                          "Goverment organization background"),
                "description": ("{} has government background").format(
                    self.get_person_name()),
                "score": 0
            }
            now = pendulum.now()
            if (now - pendulum.parse(last_field_date)).in_months() <= 24:
                heuristic['score'] = 10
            elif (now - pendulum.parse(last_field_date)).in_months() > 24 and (
                    now - pendulum.parse(last_field_date)).in_months() <= 36:
                heuristic['score'] = 9
            elif (now - pendulum.parse(last_field_date)).in_months() > 36 and (
                    now - pendulum.parse(last_field_date)).in_months() <= 60:
                heuristic['score'] = 8
            elif (now - pendulum.parse(last_field_date)).in_months() > 60 and (
                    now - pendulum.parse(last_field_date)).in_months() <= 82:
                heuristic['score'] = 7
            elif (now - pendulum.parse(last_field_date)).in_months() > 82 and (
                    now - pendulum.parse(last_field_date)).in_months() <= 90:
                heuristic['score'] = 6
            elif (now - pendulum.parse(last_field_date)).in_months() > 90:
                heuristic['score'] = 5

            self.alerts.ineligible_occupation = update_heuristics_score(
                self.alerts.ineligible_occupation, heuristic)
