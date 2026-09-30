from business_rules.variables import boolean_rule_variable

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import create_positions_list_additive
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class TeamworkVariables(PersonBaseVariables):

    @boolean_rule_variable()
    def person_has_teamwork(self):
        positions = create_positions_list_additive(self.person)

        if positions:
            work_experience = {
                "hash": str(positions),
                "work_experience": positions
            }
            logger.debug('Rules engine: TeamworkVariables'
                         ' teamwork for positions')
            try:
                ds_response = ds_app_api.ds_request.team_work_experience(
                    body=work_experience,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            if ds_response_body:
                if teamwork_experience := ds_response_body.get(
                        "teamwork_experience"):
                    for position in teamwork_experience:
                        if position.get("has_teamwork_experience"):
                            return True
        return False
