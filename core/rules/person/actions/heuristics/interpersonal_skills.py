from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT


from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (update_evaluation_factors,
                                     calculate_skill_score,
                                     build_post_photo_list,
                                     get_cover_photos)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class InterpersonalSkillsActions(PersonBaseActions):

    @rule_action(params={"social_photos": FIELD_SELECT}
                 )
    def set_person_is_sociable(self, social_photos):
        score = 6
        if bio_details := self.person.biographic_details:
            if work := bio_details.work:
                if linkedin_work := work.linkedin_work:
                    if skills := linkedin_work.skills:
                        for skill_model in skills:
                            if skill_model.name.lower(
                            ) == 'interpersonal skills':
                                score += 1
                                if endorser_count := (skill_model.
                                                      endorser_count):
                                    if endorser_count >= 3:
                                        score += 1
                            if skill_model.name.lower() == 'teamwork':
                                teamwork_score = calculate_skill_score(
                                    'teamwork', skill_model)
                                if teamwork_score >= 8:
                                    score += 1
                elif xing_work := work.xing_work:
                    if skills := xing_work.skills.soft_skills:
                        for skill_model in skills:
                            if skill_model.name.lower(
                            ) == 'interpersonal skills':
                                score += 1
                            if skill_model.name.lower() == 'teamwork':
                                teamwork_score = calculate_skill_score(
                                    'teamwork', skill_model)
                                if teamwork_score >= 8:
                                    score += 1
        if visuals := self.person.personal_details.visuals:
            cover_photos = get_cover_photos(visuals)
            if cover_photos:
                cover_list = [{"hash": photo, "source": photo}
                              for photo in cover_photos]
                logger.debug('Rules engine: InterpersonalSkillsActions'
                             ' sociable_events in cover photos')
                try:
                    ds_response = ds_app_api.ds_request.sociable_events(
                        body=cover_list,
                        headers={
                            'x-remote-context': build_person_urn(
                                self.person.id)
                        }
                    )
                    cover_resp = ds_response.body
                except Exception:
                    cover_resp = {}
                for photo in cover_resp:
                    if photo.get("type") in social_photos:
                        score += 1
                pass
        if posts := self.person.posts:
            photo_list = build_post_photo_list(posts)
            if photo_list:
                logger.debug('Rules engine: InterpersonalSkillsActions'
                             ' sociable_events in post photos')
                try:
                    ds_response = ds_app_api.ds_request.sociable_events(
                        body=photo_list,
                        headers={
                            'x-remote-context': build_person_urn(
                                self.person.id)
                        }
                    )
                    photo_resp = ds_response.body
                except Exception as e:
                    print(str(e))
                    photo_resp = {}
                social_list = []
                for photo in photo_resp:
                    # TODO: REAL-826 photo could be a string and raise error!
                    if (isinstance(photo, dict) and photo.get("type") in
                            social_photos):
                        social_list.append(photo)

                social_count = len(social_list)

                photo_count = len(photo_list)

                social_percentage = social_count / photo_count
                if social_percentage >= 0.15:
                    score += 1
        try:
            if teamwork := self.evaluation.teamwork:
                if teamwork.score >= 8:
                    score += 1
        except Exception:
            pass

        if score:
            score = min(score, 10)

            factor = {
                "title": ("{} shows sociable behaviour").format(
                    self.get_person_name()),
                "score": score
            }
            self.evaluation.interpersonal_skills = update_evaluation_factors(
                self.evaluation.interpersonal_skills, factor)
