from typing import List
from urllib.parse import urlparse
from business_rules.actions import rule_action
from business_rules.fields import FIELD_SELECT

from core.models.connections import FacebookConnection
from core.models.flags import Factor, FactorSource, FlagSubCategory
from core.models.interests import Page
from core.rules.person.utils import (
    build_intro_dict,
)
from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils.interests_utils import (
    build_fb_pages_photo_text_list_extremism,
)
from core.rules.person.utils.posts_utils import build_post_photo_text_list_extremism
from core.rules.person.utils.update_flag_category import update_person_flag
from core.utils import build_person_urn

from ..base import PersonBaseActions


class IslamicExtremismActions(PersonBaseActions):
    @rule_action(
        params={"jihadi_terms": FIELD_SELECT,
                "salafi_religious_terms": FIELD_SELECT}
    )
    def set_person_islamic_extremism(self, jihadi_terms, salafi_religious_terms):
        post_list = []
        intro_dict = {}
        interests_list = []
        jihadi_terms_entities = []
        islamist_terms_entities = []
        jihadi_in_intro_pages = []
        salafi_in_intro_pages = []
        # ds_jihadi_keys = [
        #     "jihadist_extrimism_text",
        #     "jihadist_extrimism_image",
        # ]
        jihadi_units_count = 0
        ds_jihadi_counts_keys = [
            "jihadist_extrimism_text_count",
            "jihadist_extrimism_image_count",
        ]
        # ds_islamist_keys = ["islamist_extrimism_text", "islamist_extrimism_image"]
        islamist_units_count = 0
        ds_islamist_counts_keys = [
            "islamist_extrimism_text_count",
            "islamist_extrimism_image_count",
        ]
        sub_categories: List[FlagSubCategory] = []
        score = 0
        try:
            post_list = build_post_photo_text_list_extremism(self.person.posts)
            posts_res = ds_app_api.ds_request.extremism(
                body=post_list["posts_list"],
                headers={"x-remote-context": build_person_urn(self.person.id)},
            )
            posts_body = posts_res.body
            for i, post_res in enumerate(posts_body):
                for key in ds_jihadi_counts_keys:
                    if post_res.get(key) > 0:
                        term_post = post_list["posts_detected"][i]
                        jihadi_terms_entities.append(term_post)
                        jihadi_units_count += post_res.get(key)
            for i, post_res in enumerate(posts_body):
                for key in ds_islamist_counts_keys:
                    if post_res.get(key) > 0:
                        islamist_units_count += post_res.get(key)
                        term_post = post_list["posts_detected"][i]
                        islamist_terms_entities.append(term_post)
        except Exception:
            pass
        try:
            intro_dict = build_intro_dict(
                self.person.biographic_details.description_bio_intro
            )
            intro_text_list = [intro for intro in intro_dict.values()]
            intro_req = [
                {"hash": k, "text": str(v)}
                for k, v in intro_dict.items()
                if v in intro_text_list
            ]
            intro_res = ds_app_api.ds_request.extremism(
                body=intro_req,
                headers={"x-remote-context": build_person_urn(self.person.id)},
            )
            intro_body = intro_res.body
            for intro_res in intro_body:
                for key in ds_jihadi_counts_keys:
                    if intro_res.get(key) > 0:
                        term_key = intro_res.get("hash")
                        jihadi_in_intro_pages.append(
                            {term_key: intro_dict[term_key]})
                        jihadi_units_count += intro_res.get(key)
                for key in ds_islamist_counts_keys:
                    if intro_res.get(key) > 0:
                        term_key = intro_res.get("hash")
                        salafi_in_intro_pages.append(
                            {term_key: intro_dict[term_key]})
                        islamist_units_count += intro_res.get(key)

        except Exception:
            pass
        try:
            interests_list = build_fb_pages_photo_text_list_extremism(
                self.person.interests.pages
            )
            pages_res = ds_app_api.ds_request.extremism(
                body=interests_list["pages_list"],
                headers={"x-remote-context": build_person_urn(self.person.id)},
            )
            pages_body = pages_res.body
            for i, page_res in enumerate(pages_body):
                for key in ds_jihadi_counts_keys:
                    if page_res.get(key) > 0:
                        term_page = interests_list["pages_detected"][i]
                        jihadi_terms_entities.append(term_page)
                        jihadi_units_count += page_res.get(key)
            for i, page_res in enumerate(pages_body):
                for key in ds_islamist_counts_keys:
                    if page_res.get(key) > 0:
                        term_page = interests_list["pages_detected"][i]
                        islamist_terms_entities.append(term_page)
                        # salafi_in_intro_pages += 1
                        islamist_units_count += page_res.get(key)
        except Exception:
            pass
        score = 0

        if jihadi_terms_entities:
            jihadi_terms_match_score = 0
            jihadi_terms_match_count = jihadi_units_count

            if jihadi_terms_match_count > 0 and jihadi_terms_match_count <= 2:
                jihadi_terms_match_score += 3
            if jihadi_terms_match_count >= 3 and jihadi_terms_match_count <= 5:
                jihadi_terms_match_score += 4
            if jihadi_terms_match_count >= 6 and jihadi_terms_match_count <= 7:
                jihadi_terms_match_score += 5
            if jihadi_terms_match_count >= 8:
                jihadi_terms_match_score += 6
            if jihadi_in_intro_pages:
                jihadi_terms_match_score += 1
            score += jihadi_terms_match_score
            process_terms(
                jihadi_terms_entities,
                sub_categories,
                "Jihadi",
                jihadi_terms_match_score,
            )

        if islamist_terms_entities:
            islamist_terms_match_score = 0
            islamist_terms_match_count = islamist_units_count
            match islamist_terms_match_count:
                case x if 0 < x <= 2:
                    islamist_terms_match_score += 1
                case x if 3 <= x <= 5:
                    islamist_terms_match_score += 2
                case x if 6 <= x <= 7:
                    islamist_terms_match_score += 4
                case x if x >= 8:
                    islamist_terms_match_score += 5
            if salafi_in_intro_pages:
                islamist_terms_match_score += 1
            score += islamist_terms_match_score
            process_terms(
                islamist_terms_entities,
                sub_categories,
                "Islamist",
                islamist_terms_match_score,
            )
        self.flag.islamic_extremism = update_person_flag(
            self.flag.islamic_extremism,
            sub_categories,
            category="Islamic Extremism",
            description=(
                "Terms suspected as Salafi-Jihadist terms detected. Frequent use of such terms may indicate radicalization and potential security risk."
            ),
            sub_category_to_delete="Islamic Extremism",
        )

    @rule_action(
        params={
            "designated_groups_a": FIELD_SELECT,
            "designated_groups_b": FIELD_SELECT,
        }
    )
    def set_person_extremism_designated_groups(
        self, designated_groups_a, designated_groups_b
    ):
        score = 0
        designated_groups_a_matches: List[Page] = []
        designated_groups_b_matches: List[Page] = []
        try:
            try:
                if interests := self.person.interests:
                    if pages := interests.pages:
                        for page in pages:
                            if (page.fb_page_id in designated_groups_a) or (
                                (
                                    urlparse(str(page.fb_page_url)
                                             ).path.lstrip("/")
                                    in designated_groups_a
                                )
                                if page.fb_page_url is not None
                                else False
                            ):
                                designated_groups_a_matches.append(page)
                            if (page.fb_page_id in designated_groups_b) or (
                                (
                                    urlparse(str(page.fb_page_url)
                                             ).path.lstrip("/")
                                    in designated_groups_b
                                )
                                if page.fb_page_url is not None
                                else False
                            ):
                                designated_groups_b_matches.append(page)
            except Exception:
                pass
            try:
                if connections := self.person.connections:
                    if (
                        not connections
                        or not connections.following
                        or not connections.following.facebook
                    ):
                        pass
                    for follow in connections.following.facebook:
                        if follow.facebook_user_id in designated_groups_a:
                            designated_groups_a_matches.append(follow)
                        if follow.facebook_user_id in designated_groups_b:
                            designated_groups_b_matches.append(follow)
            except Exception:
                pass
            if designated_groups_a_matches or designated_groups_b_matches:
                sub_categories: List[FlagSubCategory] = []
                if designated_groups_a_matches:
                    designated_groups_a_score = 0
                    match len(designated_groups_a_matches):
                        case 1:
                            designated_groups_a_score += 2
                        case 2:
                            designated_groups_a_score += 4
                        case 3:
                            designated_groups_a_score += 5
                        case _ if len(designated_groups_a_matches) >= 4:
                            designated_groups_a_score += 6
                    score += designated_groups_a_score
                    designated_groups_a_sub_category = FlagSubCategory(
                        sub_category="Designated Online Groups A (Jihadist Online Communities)",
                        description=(
                            "Person follows one or more extremist groups"
                            " or pages from Designated Groups A list."
                        ),
                        severity=designated_groups_a_score,
                        factors=[],
                    )
                    for group in designated_groups_a_matches:
                        if isinstance(group, FacebookConnection):
                            designated_groups_a_sub_category.factors.append(
                                Factor(
                                    field="friend",
                                    platform="facebook",
                                    source={
                                        "insight": (
                                            "Person follows extremist"
                                            " designated groups or pages"
                                            " from Designated Groups A list."
                                        ),
                                        "url": group.facebook_profile_url,
                                        "photo": group.facebook_profile_picture,
                                        "id": group.facebook_user_id,
                                        "text": group.facebook_full_name,
                                    },
                                    success=True,
                                    ratio=1,
                                )
                            )
                        else:
                            designated_groups_a_sub_category.factors.append(
                                Factor(
                                    field="page",
                                    platform="facebook",
                                    source={
                                        "insight": (
                                            "Person follows extremist"
                                            " designated groups or pages"
                                            " from Designated Groups A list."
                                        ),
                                        "id": group.fb_page_id,
                                        "text": group.fb_page_name,
                                        "url": group.fb_page_url,
                                        "photo": group.fb_page_profile_photo,
                                    },
                                    success=True,
                                    ratio=1,
                                )
                            )
                    sub_categories.append(designated_groups_a_sub_category)

                if designated_groups_b_matches:
                    designated_groups_b_score = 0
                    match len(designated_groups_b_matches):
                        case 1:
                            designated_groups_b_score += 1.5
                        case 2:
                            designated_groups_b_score += 2
                        case 3:
                            designated_groups_b_score += 3
                        case 4:
                            designated_groups_b_score += 4
                        case _ if len(designated_groups_b_matches) >= 5:
                            designated_groups_b_score += 5

                    score += designated_groups_b_score

                    designated_groups_b_sub_category = FlagSubCategory(
                        sub_category="Designated Online Groups B (Radical Narratives)",
                        description=(
                            "Person follows one or more extremist groups"
                            " or pages from Designated Groups B list."
                        ),
                        severity=designated_groups_b_score,
                        factors=[],
                    )

                    for group in designated_groups_b_matches:
                        if isinstance(group, FacebookConnection):
                            designated_groups_b_sub_category.factors.append(
                                Factor(
                                    field="friend",
                                    platform="facebook",
                                    source={
                                        "insight": (
                                            "Person follows extremist"
                                            " designated groups or pages"
                                            " from Designated Groups B list."
                                        ),
                                        "url": group.facebook_profile_url,
                                        "photo": group.facebook_profile_picture,
                                        "id": group.facebook_user_id,
                                        "text": group.facebook_full_name,
                                    },
                                    success=True,
                                    ratio=1,
                                )
                            )
                        else:
                            designated_groups_b_sub_category.factors.append(
                                Factor(
                                    field="page",
                                    platform="facebook",
                                    source={
                                        "insight": (
                                            "Person follows extremist"
                                            " designated groups or pages"
                                            " from Designated Groups B list."
                                        ),
                                        "id": group.fb_page_id,
                                        "text": group.fb_page_name,
                                        "url": group.fb_page_url,
                                        "photo": group.fb_page_profile_photo,
                                    },
                                    success=True,
                                    ratio=1,
                                )
                            )
                    sub_categories.append(designated_groups_b_sub_category)
                self.flag.islamic_extremism = update_person_flag(
                    self.flag.islamic_extremism,
                    sub_categories=sub_categories,
                    category="Islamic Extremism",
                    description=(
                        "Person follows extremist designated groups or pages."
                    ),
                    sub_category_to_delete="Islamic Extremism",
                )
        except Exception:
            pass


def get_nested_attr(obj, attr_chain, default=None):
    current = obj
    for attr in attr_chain.split("."):
        current = getattr(current, attr, None)
        if current is None:
            return default
    return current


def process_terms(
    entities,
    sub_categories: List[FlagSubCategory],
    insight_text,
    score,
    is_intro: bool = False,
):
    if not entities or score < 0.01:
        return

    sub_category = FlagSubCategory(
        sub_category=f"{insight_text} Terms",
        description=(
            f"Terms suspected as {insight_text.lower()} terms detected. Frequent use of such terms may indicate radicalization and potential security risk."
        ),
        severity=score,
        factors=[],
    )
    if is_intro:

        for terms in entities:
            for key, value in terms.items():
                factor = Factor(
                    field=key,
                    source={"insight": f"Person has {insight_text} terms. {value}"},
                    success=True,
                    ratio=1,
                )
                sub_category.factors.append(factor)
    else:

        insight_base = f"{insight_text} term"

        # Configuration for “Post”-type sources
        post_configs = [
            {
                "text_attr": "fb_post_text",
                "platform": "facebook",
                "field": "post",
                "photo_chains": [
                    "fb_post_photo.fb_photo.url",
                    "fb_uploaded_photo.fb_photo.url",
                ],
                "insight_prefix": "Post shows",
                "url_attr": "fb_post_url",
            },
            {
                "text_attr": "instagram_post_text",
                "platform": "instagram",
                "field": "post",
                "photo_chains": ["instagram_post_photo"],
                "insight_prefix": "Post shows",
            },
            {
                "text_attr": "linkedin_post_text",
                "platform": "linkedin",
                "field": "post",
                "photo_chains": ["linkedin_post_photo"],
                "url_attr": "linkedin_post_url",
                "insight_prefix": "Post shows",
            },
        ]

        for entity in entities:
            try:
                for cfg in post_configs:
                    text = getattr(entity, cfg["text_attr"], None)
                    photo = None
                    for chain in cfg.get("photo_chains", []):
                        photo = get_nested_attr(entity, chain)
                        if photo:
                            break
                    if not text and not photo:
                        continue
                    factor = Factor(
                        field=cfg["field"],
                        platform=cfg["platform"],
                        success=True,
                        ratio=1,
                    )

                    factor.source = FactorSource(
                        insight=f"{cfg['insight_prefix']} {insight_base}",
                        text=text,
                        photo=photo,
                    )

                    if "url_attr" in cfg:
                        url = getattr(entity, cfg["url_attr"], None)
                        if url:
                            factor.source.url = url
                    sub_category.factors.append(factor)
                page_name = getattr(entity, "fb_page_name", None)
                if page_name:
                    factor = Factor(
                        field="page", platform="facebook", success=True, ratio=1
                    )
                    factor.source = FactorSource(
                        insight=f"Liked Page {page_name} shows {insight_base}",
                        photo=getattr(entity, "fb_page_profile_photo", None),
                        url=getattr(entity, "fb_page_url", None),
                    )
                    sub_category.factors.append(factor)

            except Exception as e:
                pass

    sub_categories.append(sub_category)
