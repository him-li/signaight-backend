from business_rules.variables import boolean_rule_variable
from business_rules.fields import FIELD_SELECT

from core.rules.person.utils import (
    build_post_photo_text_list,
    build_intro_dict,
    build_fb_pages_photo_text_list,
    get_cover_photos_ds_app,
    get_profile_photos_ds_app)
from core.clients.ds_app import api as ds_app_api
from core.utils import build_person_urn

from ..base import PersonBaseVariables


class ExtremismVariables(PersonBaseVariables):
    @boolean_rule_variable(
        label='Person has posts showing extremism',
        params={
            'jihadi_terms': FIELD_SELECT,
            'salafi_religious_terms': FIELD_SELECT
        }
    )
    def person_has_islamic_extremism(self,
                                     jihadi_terms,
                                     salafi_religious_terms):
        ds_extremism_keys = [
            "jihadist_extrimism_text",
            "jihadist_extrimism_image",
            "islamist_extrimism_text",
            "islamist_extrimism_image"
        ]
        try:
            terms_list = [*jihadi_terms, *salafi_religious_terms]
            post_list = []
            intro_dict = {}
            interests_list = []
            try:
                post_list = build_post_photo_text_list(self.person.posts)
                post_text_list = [post.get("text") for post in post_list["posts_list"]]
                for text in post_text_list:
                    if text in terms_list:
                        return True

                ds_response = ds_app_api.ds_request.extremism(
                    body=post_list["posts_list"],
                    headers={"x-remote-context": build_person_urn(self.person.id)},
                )
                ds_body = ds_response.body
                if any(item.get(key) for key in ds_extremism_keys for
                        item in ds_body):
                    return True
            except Exception:
                pass
            try:
                intro_dict = build_intro_dict(
                    self.person.biographic_details.description_bio_intro)
                intro_text_list = [intro for intro in intro_dict.values()]
                for text in intro_text_list:
                    if text in terms_list:
                        return True
                intro_req = [
                    {"hash": k, "text": v} for k, v in
                    intro_dict.items() if v in intro_text_list
                ]
                ds_response = ds_app_api.ds_request.extremism(
                    body=intro_req,
                    headers={
                        'x-remote-context': build_person_urn(
                            self.person.id)
                    }
                )
                ds_body = ds_response.body
                if any(item.get(key) for key in ds_extremism_keys for
                        item in ds_body):
                    return True
            except Exception:
                pass
            try:
                interests_list = build_fb_pages_photo_text_list(
                    self.person.interests.pages)
                interests_text_list = [page.get("text")
                                       for page in interests_list]
                for text in interests_text_list:
                    if text in terms_list:
                        return True
                ds_response = ds_app_api.ds_request.extremism(
                    body=interests_list,
                    headers={
                        'x-remote-context': build_person_urn(
                            self.person.id)
                    }
                )
                ds_body = ds_response.body
                if any(item.get(key) for key in ds_extremism_keys for
                        item in ds_body):
                    return True
            except Exception:
                pass
            return False
        except Exception:
            return False

    @boolean_rule_variable(
        label='Person has references to weapons in posts'
    )
    def person_has_photos_with_weapons(self):
        post_list = []
        interests_list = []
        cover_photos = []
        profile_photos = []
        try:
            try:
                post_list = build_post_photo_text_list(self.person.posts)
                if interests := self.person.interests:
                    interests_list = build_fb_pages_photo_text_list(
                        interests.pages)
                if person_images := self.person.personal_details.visuals:
                    cover_photos = get_cover_photos_ds_app(person_images)
                    profile_photos = get_profile_photos_ds_app(person_images)
                images_list = (
                    cover_photos
                    + profile_photos
                    + post_list["posts_list"]
                    + interests_list
                )
                ds_response = ds_app_api.ds_request.check_weapons(
                    body=images_list,
                    headers={
                        'x-remote-context': build_person_urn(
                            self.person.id)
                    }
                )
                ds_body = ds_response.body
                if any(item.get("weapons") for
                        item in ds_body):
                    return True
            except Exception:
                pass
            return False

        except Exception:
            return False
