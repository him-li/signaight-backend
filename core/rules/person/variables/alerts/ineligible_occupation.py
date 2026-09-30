from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_NUMERIC, FIELD_SELECT

from core.rules.person.utils import (check_min_experience,
                                     create_positions_list_additive,
                                     create_position_model_list_additive,
                                     create_position_model_list_unique)
from core.clients.ds_app import api as ds_app_api
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class IneligibleOccupationVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person has less than minumim years of experience',
        params=[{
            'field_type': FIELD_NUMERIC,
            'name': 'min_months',
            'label': 'Minimum Months of Experience'
        }]
    )
    def person_without_minimum_experience(self, min_months=36):
        try:
            positions = create_position_model_list_unique(self.person)
            if not positions or not isinstance(positions, list):
                return True
            positions.sort(key=lambda position: position.period.date_from)
            positions.reverse()
        except Exception:
            return False
        experience_months = check_min_experience(positions)
        if experience_months < min_months:
            return True
        return False

    @boolean_rule_variable(
        label='Person has specific background',
        params=[{
            'name': 'titles',
            'field_type': FIELD_SELECT
        }]
    )
    def person_with_specific_background(self, titles):
        try:
            positions = create_position_model_list_additive(self.person)
            if not positions or not isinstance(positions, list):
                return False
        except Exception:
            return False
        for position in positions:
            for title in titles:
                if position.title and title in position.title.lower():
                    return True
        return False

    @boolean_rule_variable(
        label='Person has specific background',
        params=[{
            'name': 'fields',
            'field_type': FIELD_SELECT
        }]
    )
    def person_with_background_in_specific_company_areas(self, fields):
        positions = create_positions_list_additive(self.person)
        if positions:
            if 'government' in fields:
                work_experience = {
                    "hash": str(positions),
                    "work_experience": positions
                }
                try:
                    logger.debug('Rules engine: IneligibleOccupationVariables'
                                 ' government_experience for positions')
                    ds_response = ds_app_api.ds_request.government_experience(
                        body=work_experience,
                        headers={
                            'x-remote-context': build_person_urn(
                                self.person.id)
                        }
                    )
                    ds_response_body = ds_response.body
                    if ds_response_body:
                        if government_experience := ds_response_body.get(
                                "government_experience"):
                            for position in government_experience:
                                if position.get("has_government_experience"):
                                    return True
                except Exception as e:
                    logger.info(str(e))
            else:
                for position in positions:
                    for field in fields:
                        if field in position.get("company_name").lower():
                            return True
        return False
