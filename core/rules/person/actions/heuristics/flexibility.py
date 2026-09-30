from business_rules.actions import rule_action

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (
    update_evaluation_factors,
    create_position_model_list_additive,
    create_skills_model_list)
from business_rules.fields import FIELD_SELECT

from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class FlexibilityActions(PersonBaseActions):

    @rule_action()
    def set_person_flexibility_score(self):

        skills = create_skills_model_list(self.person)
        positions = create_position_model_list_additive(self.person)

        if skills:

            try:
                skills_score = 0
                for skill in skills:
                    if skill.name.lower() == 'flexibility':
                        skills_score += 7
                        if skill.endorser_count == 1:
                            skills_score += 1
                        if (skill.endorser_count >= 2 and
                                skill.endorser_count <= 3):
                            skills_score += 2
                        if skill.endorser_count >= 4:
                            skills_score += 3

                if skills_score:
                    if skills_score > 10:
                        skills_score = 10
                    factor = {
                        "title": (
                            "{person} has is flexibility in skills").format(
                            person=self.get_person_name()),
                        "score": skills_score
                    }

                    self.evaluation.flexibility = update_evaluation_factors(
                        self.evaluation.flexibility, factor)

            except Exception as e:
                logger.info(str(e))

        # if positions:
        #     if linkedin_work := (self.person.biographic_details.work.
        #                          linkedin_work):
        #         linkedin_work = linkedin_work.model_dump()

        #         positions = linkedin_work.get("positions")
        #         positions = [{k.replace('linkedin_', ''): v for k, v in
        #                       position.items() if not
        #                       k.startswith('linkedin_')} for position in
        #                      positions]

        #     elif xing_work := (self.person.biographic_details.work.
        #                        xing_work):
        #         xing_work = xing_work.model_dump()

        #         positions = xing_work.get("positions")
        #         positions = [{k.replace('xing_', ''): v for k, v in
        #                       position.items() if not
        #                       k.startswith('xing_')}
        #                      for position in positions]

        #     posts_list_work = {
        #         "hash": str(positions) if positions else None,
        #         "work_experience": positions,
        #     }

        #     try:
        #         logger.debug('Rules engine: FlexibilityActions'
        #                      ' flexibility_work in works')
        #         ds_response = ds_app_api.ds_request.flexibility_work(
        #             body=posts_list_work,
        #             headers={
        #                 'x-remote-context': build_person_urn(self.person.id)
        #             }
        #         )
        #         work_flexibility = ds_response.body

        #         # Calculate score
        #         work_score = 0
        #         if work_flexibility['general_flexibility']['is_flexible']:
        #             work_score = 5
        #         for flexibility in work_flexibility[
        #                 'individual_flexibility']:
        #             if flexibility['is_flexible']:
        #                 work_score += 2
        #         if work_score:
        #             if work_score > 10:
        #                 work_score = 10
        #             factor = {
        #                 "title": ("{person} has is flexible at work").format(
        #                     person=self.get_person_name()),
        #                 "score": work_score
        #             }

        #             self.evaluation.flexibility = update_evaluation_factors(
        #                 self.evaluation.flexibility, factor)

        #     except Exception as e:
        #         logger.info(str(e))

    @rule_action()
    def set_flexibility_transition_industries(self):
        positions = create_position_model_list_additive(self.person)

        if positions:
            if linkedin_work := (self.person.biographic_details.work.
                                 linkedin_work):
                linkedin_work = linkedin_work.model_dump()

                positions = linkedin_work.get("positions")
                positions = [{k.replace('linkedin_', ''): v for k, v in
                              position.items() if not
                              k.startswith('linkedin_')} for position in
                             positions]

            elif xing_work := (self.person.biographic_details.work.
                               xing_work):
                xing_work = xing_work.model_dump()

                positions = xing_work.get("positions")
                positions = [{k.replace('xing_', ''): v for k, v in
                              position.items() if not
                              k.startswith('xing_')}
                             for position in positions]

            posts_list_work = {
                "hash": str(positions) if positions else None,
                "work_experience": positions,
            }

            try:
                logger.debug('Rules engine: FlexibilityActions'
                             ' flexibility_transition_industries in works')
                ds_response = (
                    ds_app_api.ds_request.flexibility_transition_industries(
                        body=posts_list_work,
                        headers={
                            'x-remote-context': build_person_urn(self.person.id)
                        }
                    ))
                work_flexibility = ds_response.body

                # Calculate score
                score = 0
                industries_count = work_flexibility.get("industries_count")
                industries_proximity = work_flexibility.get(
                    "industries_proximity")

                if industries_count == 2:
                    score += 3
                elif industries_count == 3:
                    score += 4
                elif industries_count == 4:
                    score += 5
                elif industries_count >= 5:
                    score += 6

                if industries_proximity.strip() == "low":
                    score += 5
                elif industries_proximity.strip() == "medium-low":
                    score += 4
                elif industries_proximity.strip() == "medium":
                    score += 2
                elif industries_proximity.strip() == "medium-high":
                    score += 1

                if score:
                    if score > 10:
                        score = 10
                    factor = {
                        "title": ("{person}'s work experience shows"
                                  " flexibility when transitioning "
                                  "between industries").format(
                            person=self.get_person_name()),
                        "score": score
                    }

                    self.evaluation.flexibility = update_evaluation_factors(
                        self.evaluation.flexibility, factor)

            except Exception as e:
                logger.info(str(e))

    @rule_action(params={
        "test_skills": FIELD_SELECT
    })
    def set_person_flexibility_skill_set(self, test_skills: dict):
        skills = create_skills_model_list(self.person)

        if skills:
            skills_names = [skill.name for skill in skills]
            post_skills = {
                "hash": str(skills),
                "skills": skills_names,
                "test_skills": [skill for skill in test_skills.keys()]
            }

            try:
                logger.debug('Rules engine: FlexibilityActions'
                             ' flexibility_skill_set in skills')
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

                for index, skill in enumerate(flexible_skills):
                    if skill in test_skills:
                        try:
                            skill_score = test_skills[skill]
                            skill_endorsers = skills[index].endorser_count
                            if skill_endorsers and skill_endorsers > 4:
                                score += skill_score * 1.5
                            else:
                                score += skill_score
                        except Exception:
                            pass

                if score:
                    if score > 10:
                        score = 10
                    factor = {
                        "title": ("{person} Skill Set Analysis"
                                  ).format(person=self.get_person_name()),
                        "score": score
                    }

                    self.evaluation.flexibility = update_evaluation_factors(
                        self.evaluation.flexibility, factor)

            except Exception as e:
                logger.info(str(e))
