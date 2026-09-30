from datetime import datetime
import pendulum
from business_rules.actions import rule_action
from business_rules.fields import FIELD_TEXT

from core.models.flags import FlagSubCategory
from core.rules.person.utils import update_heuristics_score, build_post_photo_text_list
from core.clients.ds_app import api as ds_app_api
from core.logging import logger
from core.rules.person.utils.update_flag_category import update_person_flag
from core.utils import build_person_urn

from ..base import PersonBaseActions


class AntiCountiStatementsActions(PersonBaseActions):

    @rule_action(params={"country": FIELD_TEXT})
    def set_person_anti_country(self, country):
        posts = self.person.posts
        if posts:
            score = 0
            try:
                posts_list = build_post_photo_text_list(posts)
                anti_country_posts = []

                if country == "IL":
                    logger.debug(
                        "Rules engine: AntiCountiStatementsActions"
                        " anti_israel for posts"
                    )
                    ds_response = ds_app_api.ds_request.anti_israel(
                        body=posts_list["posts_list"],
                        headers={
                            "x-remote-context": build_person_urn(self.person.id)},
                    )
                    ds_response_body = ds_response.body
                    anti_posts = 0
                    for i, resp in enumerate(ds_response_body):
                        if resp.get("is_anti_israel"):
                            anti_posts += 1

                            post = posts_list["posts_detected"][i]
                            anti_country_posts.append(post)

                            if post_author := post.post_author:
                                try:
                                    if author_url := (post_author.fb_profile_url):
                                        if person_url := (
                                            self.person.network_signature.url.facebook_profile_url
                                        ):
                                            if author_url == person_url:
                                                score += 1
                                    elif author_url := (
                                        post_author.linkedin_profile_url
                                    ):
                                        if person_url := (
                                            self.person.network_signature.url.linkedin_profile_url
                                        ):
                                            if author_url == person_url:
                                                score += 1
                                    elif author_id := post_author.fb_user_id:
                                        if person_id := (
                                            self.person.network_signature.user_id.facebook_user_id
                                        ):
                                            if author_id == person_id:
                                                score += 1
                                    elif author_id := (post_author.twitter_user_id):
                                        if person_id := (
                                            self.person.network_signature.user_id.twitter_user_id
                                        ):
                                            if author_id == person_id:
                                                score += 1
                                except Exception:
                                    pass

                            try:
                                if author_id := post.instagram_user_id:
                                    if person_id := (
                                        self.person.network_signature.user_id.instagram_user_id
                                    ):
                                        if author_id == person_id:
                                            score += 1
                            except Exception:
                                pass

                            if post.linkedin_post_publishment_date:
                                try:
                                    now = pendulum.now()
                                    publish_date = pendulum.parse(
                                        str(post.linkedin_post_publishment_date),
                                        strict=False,
                                    )
                                    month_diff = (
                                        now - publish_date).in_months()
                                    if month_diff < 12:
                                        score += 1
                                except Exception:
                                    pass

                    if anti_posts:
                        if anti_posts == 1:
                            score += 7
                        elif anti_posts >= 2:
                            score += 8

                    if score:
                        score = min(score, 10)

                        heuristic = {
                            "title": ("{} has anti Israel posts").format(
                                self.get_person_name()
                            ),
                            "description": "Posts show anti Israel statements",
                            "score": score,
                        }
                        (self.alerts.anti_israel_statements) = update_heuristics_score(
                            self.alerts.anti_israel_statements, heuristic
                        )
                        factors_data = []
                        for post in anti_country_posts:
                            preview_text = (
                                post.fb_post_text
                                if post.fb_post_text
                                else (
                                    post.instagram_post_text
                                    if post.instagram_post_text
                                    else (
                                        post.linkedin_post_text
                                        if post.linkedin_post_text
                                        else ""
                                    )
                                )
                            )
                            image = (
                                post.fb_post_photo.fb_photo.url
                                if post.fb_post_photo
                                else (
                                    post.instagram_post_photo
                                    if post.instagram_post_photo
                                    else (
                                        post.linkedin_post_photo
                                        if post.linkedin_post_photo
                                        else None
                                    )
                                )
                            )
                            if preview_text or image:
                                factor_data = {
                                    "ratio": score,
                                    "field": "post",
                                    "platform": (
                                        "facebook"
                                        if post.fb_post_text
                                        else (
                                            "instagram"
                                            if post.instagram_post_text
                                            else (
                                                "linkedin"
                                                if post.linkedin_post_text
                                                else ""
                                            )
                                        )
                                    ),
                                    "source": {
                                        "url": (post.fb_post_url or post.linkedin_post_url or None),
                                        "insight": "Post show anti Israel statements",
                                        "text": preview_text,
                                        "photo": image,
                                        "date": (
                                            datetime.utcfromtimestamp(
                                                post.fb_post_publish_at_date
                                            )
                                            if post.fb_post_publish_at_date
                                            else None
                                        ),
                                    },
                                }
                                factors_data.append(factor_data)
                        try:
                            sub_category = FlagSubCategory(
                                sub_category="Anti Israel Statements",
                                description=(
                                    "Posts show anti Israel statements"),
                                factors=factors_data,
                                severity=float(min(score, 10.0)),
                            )
                            self.flag.anti_israel_statements = update_person_flag(
                                self.flag.anti_israel_statements,
                                sub_categories=[sub_category],
                                category="Anti Israel Statements",
                                description="Person has social media posts with anti Israel statements.",
                                sub_category_to_delete="Posts show anti Israel statements"
                            )
                        except Exception as e:
                            print("error", e)

                elif country == "US":
                    logger.debug(
                        "Rules engine: AntiCountiStatementsActions"
                        " anti_usa for posts"
                    )
                    ds_response = ds_app_api.ds_request.anti_usa(
                        body=posts_list["posts_list"],
                        headers={
                            "x-remote-context": build_person_urn(self.person.id)},
                    )
                    ds_response_body = ds_response.body
                    anti_posts = 0
                    for i, resp in enumerate(ds_response_body):
                        if resp.get("is_anti_usa"):
                            anti_posts += 1

                            post = posts_list["posts_detected"][i]
                            anti_country_posts.append(post)

                    if anti_posts:
                        if anti_posts <= 2:
                            score += 7
                        elif anti_posts >= 3 and anti_posts <= 4:
                            score += 8
                        elif anti_posts == 5:
                            score += 9
                        elif anti_posts >= 6:
                            score += 10

                    if score:
                        score = min(score, 10)

                        heuristic = {
                            "title": ("{} has anti USA posts").format(
                                self.get_person_name()
                            ),
                            "description": "Posts show anti USA statements",
                            "score": score,
                        }
                        (self.alerts.anti_usa_statements) = update_heuristics_score(
                            self.alerts.anti_usa_statements, heuristic
                        )

                        factors_data = []
                        for post in anti_country_posts:
                            factor_data = {
                                "ratio": score,
                                "field": "post",
                                "platform": (
                                    "facebook"
                                    if post.fb_post_text
                                    else (
                                        "instagram"
                                        if post.instagram_post_text
                                        else (
                                            "linkedin"
                                            if post.linkedin_post_text
                                            else ""
                                        )
                                    )
                                ),
                                "source": {
                                    "url": (post.fb_post_url or post.linkedin_post_url or None),
                                    "insight": "Posts show anti USA statements",  # noqa
                                    "text": (
                                        post.fb_post_text
                                        if post.fb_post_text  # noqa
                                        else (
                                            post.instagram_post_text
                                            if post.instagram_post_text  # noqa
                                            else (
                                                post.linkedin_post_text
                                                if post.linkedin_post_text
                                                else ""
                                            )
                                        )
                                    ),  # noqa
                                    "photo": (
                                        post.fb_post_photo.fb_photo.url
                                        if post.fb_post_photo  # noqa
                                        else (
                                            post.instagram_post_photo
                                            if post.instagram_post_photo  # noqa
                                            else (
                                                post.linkedin_post_photo
                                                if post.linkedin_post_photo
                                                else None
                                            )
                                        )
                                    ),  # noqa
                                    "date": (
                                        datetime.utcfromtimestamp(
                                            post.fb_post_publish_at_date
                                        )
                                        if post.fb_post_publish_at_date
                                        else None
                                    ),
                                },
                            }
                            factors_data.append(factor_data)
                        sub_category = FlagSubCategory(
                            sub_category="Anti USA Statements",
                            description=("Posts show anti USA statements"),
                            factors=factors_data,
                            severity=float(min(score, 10))
                        )
                        self.flag.anti_usa_statements = update_person_flag(
                            self.flag.anti_usa_statements,
                            sub_categories=[sub_category],
                            category="Anti USA Statements",
                            description=(
                                "Person has social media posts with"
                                " anti USA statements."
                            ),
                            max_value=10.0
                        )

            except Exception as e:
                logger.info(str(e))

        return
