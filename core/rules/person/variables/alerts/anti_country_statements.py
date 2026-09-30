from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_TEXT

from core.rules.person.utils import build_post_photo_text_list
from core.clients.ds_app import api as ds_app_api
from core.logging import logger
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class AntiCountryStatementsVariables(PersonBaseVariables):

    @boolean_rule_variable(
        params={"country": FIELD_TEXT}
    )
    def check_person_anti_country(self, country):
        posts = self.person.posts
        if posts:
            try:
                posts_list = build_post_photo_text_list(posts)
                # TODO: remove hardcoded country code and make it as request
                # option
                if country == "IL":
                    logger.debug('Rules engine: AntiCountryStatementsVariables'
                                 ' anti_israel for posts')
                    try:
                        ds_response = ds_app_api.ds_request.anti_israel(
                            body=posts_list["posts_list"],
                            headers={
                                'x-remote-context': 
                                    build_person_urn(self.person.id)
                            }
                        )
                        ds_response_body = ds_response.body
                        for resp in ds_response_body:
                            if resp.get("is_anti_israel"):
                                return True
                    except Exception:
                        return False
                if country == "US":
                    logger.debug('Rules engine: AntiCountryStatementsVariables'
                                 ' anti_usa for posts')
                    try:
                        ds_response = ds_app_api.ds_request.anti_usa(
                            body=posts_list["posts_list"],
                            headers={
                                'x-remote-context': 
                                    build_person_urn(self.person.id)
                            }
                        )
                        ds_response_body = ds_response.body
                        for resp in ds_response_body:
                            if resp.get("is_anti_usa"):
                                return True
                    except Exception:
                        return False

            except Exception as e:
                logger.info(str(e))
        return False
