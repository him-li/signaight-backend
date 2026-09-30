from business_rules.actions import rule_action

from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils import (
    update_evaluation_factors_weighted_average,
    create_skills_model_list,
    create_positions_list_additive)
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseActions


class ResilienceActions(PersonBaseActions):

    @rule_action()
    def set_person_optimism(self):
        posts = self.person.posts

        posts_list = [
            {
                "hash": (post.fb_post_text if post.fb_post_text else
                         post.linkedin_post_text if post.linkedin_post_text
                         else post.instagram_post_text if
                         post.instagram_post_text
                         else post.twitter_post_text if
                         post.twitter_post_text
                         else None),
                "text": (post.fb_post_text if post.fb_post_text else
                         post.linkedin_post_text if post.linkedin_post_text
                         else post.instagram_post_text if
                         post.instagram_post_text
                         else post.twitter_post_text if
                         post.twitter_post_text
                         else None)
            }
            for post in posts
        ]
        posts_list = [post for post in posts_list if post.get("hash")]

        try:
            logger.debug('Rules engine: ResilienceActions'
                         ' sentiment_analysis in posts')
            ds_response = ds_app_api.ds_request.sentiment_analysis(
                body=posts_list,
                headers={'x-remote-context': build_person_urn(self.person.id)}
            )
            sentiment_list = ds_response.body

            pos_probas = [result.get('probas', {}).get('POS', None) for
                          result in sentiment_list if 'POS' in
                          result.get('probas', {}) and
                          isinstance(result, dict)]

            average_pos_proba = (sum(pos_probas) / len(pos_probas) if
                                 pos_probas else 0)

            optimism_score = average_pos_proba * 10

            optimism_score = round(optimism_score, 0)
            if optimism_score:

                factor = {
                    "title": ("{person}'s posts indicate optimism".format(
                        person=self.get_person_name(),
                    )),
                    "score": optimism_score
                }
                self.evaluation.resilience = (
                    update_evaluation_factors_weighted_average(
                        self.evaluation.resilience, factor))
        except Exception as e:
            logger.info(str(e))

    @rule_action()
    def set_person_tuned_resilience_score(self):
        try:
            linkedin_experience = create_positions_list_additive(self.person)
            linkedin_skills = [skill.name
                               for skill in
                               create_skills_model_list(self.person)]

            req_data = {
                'linkedin_experience': linkedin_experience,
                'linkedin_skills': linkedin_skills,
            }
            req_body = {'persons': [req_data], "hash": str(req_data)}
            res = ds_app_api.ds_request.resilience_tuned_score(
                body=req_body)
            res_body = res.body
            for person in res_body.get("scores"):
                score = person.get("score")

            if score:
                score = score + 3
                if score > 10:
                    score = 10
                factor = {
                    "title": (
                        "{} work experience and skills show "
                        "resilience.".format(
                            self.get_person_name())),
                    "score": score
                }
                self.evaluation.resilience = (
                    update_evaluation_factors_weighted_average(
                        self.evaluation.resilience, factor))
        except Exception as e:
            logger.info(e)
