import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (
    update_evaluation_factors, create_skills_model_list)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class WorkUnderPressureActions(PersonBaseActions):

    @rule_action()
    def set_person_work_under_pressure(self):
        positions = []
        try:
            if linkedin_work := (self.person.biographic_details.work.
                                 linkedin_work):
                linkedin_work = linkedin_work.model_dump()
                _ = (positions.extend(linkedin_work.get("positions", []))
                     if linkedin_work.get("positions") else [])
        except Exception:
            pass
        try:
            if xing_work := self.person.biographic_details.work.xing_work:
                xing_work = xing_work.model_dump()
                _ = (positions.extend(xing_work.get("positions", []))
                     if xing_work.get("positions") else positions)
        except Exception:
            pass
        for position in positions:
            if company_logo_url := position.get("company_logo_url"):
                position['company_logo_url'] = str(company_logo_url)
            if linkedin_company_url := position.get("linkedin_company_url"):
                position['linkedin_company_url'] = str(linkedin_company_url)
            if xing_company_url := position.get("xing_company_url"):
                position['xing_company_url'] = str(xing_company_url)
        work_experience = {
            "hash": str(positions),
            "work_experience": positions
        }
        logger.debug('Rules engine: WorkUnderPressureActions'
                     ' work_under_pressure in work experience')
        try:
            ds_response = ds_app_api.ds_request.work_under_pressure(
                body=work_experience,
                headers={'x-remote-context': build_person_urn(self.person.id)}
            )
            work_under_pressure = ds_response.body
        except Exception:
            work_under_pressure = {}
        score = 0
        if work_under_pressure and isinstance(work_under_pressure, dict):
            if response := work_under_pressure.get("work_under_pressure"):
                total_duration = 0
                for i, position in enumerate(response):
                    if position.get("can_work_under_pressure"):
                        if i < 2:
                            score += 1
                        position_info = positions[i]
                        if duration := position_info.get("duration"):
                            if duration.get("months") or duration.get("years"):
                                duration_months = 0
                                if years := duration.get("years"):
                                    duration_months += years * 12
                                if months := duration.get("months"):
                                    duration_months += months
                                if i < 2 and duration_months >= 24:
                                    score += 1
                                total_duration += duration_months

                        elif period := position_info.get("period"):
                            try:
                                current_date = pendulum.now().start_of('month')
                                start = pendulum.parse(
                                    period.get("date_from"),
                                    strict=False).start_of('month')
                                try:
                                    end = (pendulum.parse(
                                        period.get("date_to"),
                                        strict=False).start_of('month') if
                                        period.get("date_to") else
                                        current_date)
                                except Exception:
                                    end = pendulum.now().start_of("month")
                                duration = end.diff(start).in_months()
                                total_duration += duration
                                if i < 2 and duration >= 24:
                                    score += 1
                            except Exception as e:
                                logger.info(str(e))
                if total_duration <= 24:
                    score += 2
                if total_duration > 24 and total_duration <= 36:
                    score += 3
                if total_duration > 36 and total_duration <= 48:
                    score += 4
                if total_duration > 48 and total_duration <= 68:
                    score += 6
                if total_duration > 68 and total_duration <= 85:
                    score += 7
                if total_duration > 85:
                    score += 8

        if score:
            score = min(score, 10)

            factor = {
                "title": (
                    "{} has demonstrated work experience in roles that "
                    "require the ability to perform effectively under "
                    "pressure.").format(
                    self.get_person_name()),
                "score": score
            }
            self.evaluation.work_under_pressure = update_evaluation_factors(
                self.evaluation.work_under_pressure, factor)

    @rule_action(params={
        "test_skills": FIELD_SELECT
    })
    def set_person_work_under_pressure_skill_set(self, test_skills: dict):
        skills = create_skills_model_list(self.person)

        if skills:
            skills_names = [skill.name for skill in skills]
            post_skills = {
                "hash": str(skills),
                "skills": skills_names,
                "test_skills": test_skills
            }

            try:
                logger.debug('Rules engine: WorkUnderPressureActions'
                             ' work_under_pressure_skill_set in skills')
                ds_response = ds_app_api.ds_request.flexibility_skill_set(
                    body=post_skills,
                    headers={
                        'x-remote-context': build_person_urn(self.person.id)
                    }
                )
                ds_res_body = ds_response.body
                flexible_skills = ds_res_body.get("flexible_skills")

                # Calculate score
                score = 0
                found_skills = 0
                endorsers_count = 0

                for index, skill in enumerate(flexible_skills):
                    if skill in test_skills:
                        try:
                            found_skills += 1
                            skill_endorsers = skills[index].endorser_count
                            if skill_endorsers:
                                endorsers_count += skill_endorsers
                        except Exception:
                            pass

                if found_skills:
                    if found_skills == 2:
                        score += 6
                    elif found_skills == 3:
                        score += 7
                    elif found_skills >= 4:
                        score += 8
                    if score:
                        if endorsers_count >= 3 and endorsers_count <= 7:
                            score += 1
                        elif endorsers_count >= 8:
                            score += 2

                if score:
                    if score > 10:
                        score = 10
                    factor = {
                        "title": ("{person} Skill Set Analysis"
                                  ).format(person=self.get_person_name()),
                        "score": score
                    }

                    self.evaluation.work_under_pressure = (
                        update_evaluation_factors(
                            self.evaluation.work_under_pressure, factor))

            except Exception as e:
                logger.info(str(e))
