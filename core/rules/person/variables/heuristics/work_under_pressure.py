from business_rules.variables import boolean_rule_variable

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import create_positions_list_additive
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class WorkUnderPressureVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_work_under_pressure(self):
        positions = create_positions_list_additive(self.person)

        if positions:
            work_experience = {
                "hash": str(positions),
                "work_experience": positions
            }
            logger.debug('Rules engine: WorkUnderPressureVariables'
                         ' work_under_pressure for positions')
            try:
                ds_response = ds_app_api.ds_request.work_under_pressure(
                    body=work_experience,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            if ds_response_body:
                if work_under_pressure := ds_response_body.get(
                        "work_under_pressure"):
                    for position in work_under_pressure:
                        if position.get("can_work_under_pressure"):
                            return True
        return False
