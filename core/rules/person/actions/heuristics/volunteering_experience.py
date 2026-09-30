from business_rules.actions import rule_action

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import update_evaluation_factors
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class VolunteeringExperienceActions(PersonBaseActions):

    @rule_action()
    def set_person_with_significant_volunteering_experience(self):
        volunteering_experiences = (self.person.biographic_details.work.
                                    linkedin_work.volunteering_experiences)
        volunteering_experiences = [volunteering_experience.model_dump() for
                                    volunteering_experience in
                                    volunteering_experiences]
        logger.debug('Rules engine: VolunteeringExperienceActions'
                     ' significant volunteering experience')
        if volunteering_experiences:
            try:
                req_body = {
                    "hash": str(volunteering_experiences),
                    "volunteering_experience": volunteering_experiences
                }
                ds_response = ds_app_api.ds_request.volunteering_experience(
                    body=req_body,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_response_body = ds_response.body
            except Exception:
                ds_response_body = {}
            volunteering_risks = []
            if ds_response_body:
                if volunteering_experience := ds_response_body.get(
                        "volunteering_experience"):
                    for position in volunteering_experience:
                        if risk := position.get(
                                "volunteering_experience_risk"):
                            volunteering_risks.append(risk)
            highest_risk = ""
            if "3 very likely both risks" in volunteering_risks:
                highest_risk = "very likely both risks"
            elif "1 very likely physical risk" in volunteering_risks:
                highest_risk = "very likely physical risk"
            elif "2 very likely emotional risk" in volunteering_risks:
                highest_risk = "very likely emotional risk"
            elif "6 moderately likely both risks" in volunteering_risks:
                highest_risk = "moderately likely both risks"
            elif "4 moderately likely physical risk" in volunteering_risks:
                highest_risk = "moderately likely physical risk"
            elif "5 moderately likely emotional risk" in volunteering_risks:
                highest_risk = "moderately likely emotional risk"

            courage_score = 0
            moral_values_score = 0
            resilience_score = 0
            if highest_risk:
                if highest_risk == "very likely both risks":
                    courage_score = 10
                    moral_values_score = 10
                    resilience_score = 10
                if highest_risk == "very likely physical risk":
                    courage_score = 9
                    moral_values_score = 8
                    resilience_score = 9
                if highest_risk == "very likely emotional risk":
                    courage_score = 6
                    moral_values_score = 8
                    resilience_score = 9
                if highest_risk == "moderately likely both risks":
                    courage_score = 6
                    moral_values_score = 7
                    resilience_score = 8
                if highest_risk == "moderately likely physical risk":
                    courage_score = 5
                    moral_values_score = 6
                    resilience_score = 7
                if highest_risk == "moderately likely emotional risk":
                    courage_score = 4
                    moral_values_score = 6
                    resilience_score = 7

                if courage_score:
                    courage_factor = {
                        "title": (
                            "{}'s volunteering experience shows courage"
                        ).format(
                            self.get_person_name()),
                        "score": courage_score
                    }
                    self.evaluation.courage = update_evaluation_factors(
                        self.evaluation.courage, courage_factor)
                if moral_values_score:
                    moral_values_factor = {
                        "title": (
                            "{}'s volunteering experience shows moral values"
                        ).format(
                            self.get_person_name()),
                        "score": moral_values_score
                    }
                    self.evaluation.moral_values = update_evaluation_factors(
                        self.evaluation.moral_values, moral_values_factor)
                if resilience_score:
                    resilience_factor = {
                        "title": (
                            "{}'s volunteering experience shows resilience"
                        ).format(
                            self.get_person_name()),
                        "score": resilience_score
                    }
                    self.evaluation.resilience = update_evaluation_factors(
                        self.evaluation.resilience, resilience_factor)
