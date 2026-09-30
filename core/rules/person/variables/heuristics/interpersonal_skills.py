from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_SELECT

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (calculate_skill_score_and_check,
                                     get_cover_photos,
                                     build_post_photo_list)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class InterpersonalSkillsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        label='Person shows sociable behaviour',
        params={"social_photos": FIELD_SELECT}
    )
    def person_is_sociable(self, social_photos):
        try:
            if teamwork := self.evaluation.teamwork:
                if teamwork.score >= 8:
                    return True
        except Exception:
            pass
        try:
            if bio_details := self.person.biographic_details:
                if work := bio_details.work:
                    try:
                        if skills := work.linkedin_work.skills:
                            if calculate_skill_score_and_check(skills, 8):
                                return True
                    except Exception:
                        pass
                    try:
                        if skills := work.xing_work.skills.soft_skills:
                            if calculate_skill_score_and_check(skills, 8):
                                return True
                    except Exception:
                        pass
            if visuals := self.person.personal_details.visuals:
                cover_photos = get_cover_photos(visuals)
                if cover_photos:
                    cover_list = [{"hash": photo, "source": photo}
                                  for photo in cover_photos]
                    logger.debug('Rules engine: InterpersonalSkillsVariables'
                                 ' sociable_events for cover photos')
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
                            return True
                    pass
            if posts := self.person.posts:
                photo_list = build_post_photo_list(posts)
                if photo_list:
                    logger.debug('Rules engine: InterpersonalSkillsVariables'
                                 ' sociable_events for post photos')
                    try:
                        ds_response = ds_app_api.ds_request.sociable_events(
                            body=photo_list,
                            headers={
                                'x-remote-context': build_person_urn(
                                    self.person.id)
                            }
                        )
                        photo_resp = ds_response.body
                    except Exception:
                        photo_resp = {}
                    if photo_resp:
                        social_list = []
                        for photo in photo_resp:
                            if photo.get("type") in social_photos:
                                social_list.append(photo)

                        social_count = len(social_list)

                        photo_count = len(photo_list)

                        social_percentage = social_count / photo_count
                        if social_percentage >= 0.15:
                            return True
        except Exception:
            return False
        return False
