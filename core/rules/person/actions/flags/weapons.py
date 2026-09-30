from datetime import datetime
from typing import List
from core.models.flags import Factor, FactorSource, FlagSubCategory
from core.rules.person.actions.base import PersonBaseActions
from business_rules.actions import rule_action
from core.rules.person.utils import (
    get_cover_photos_ds_app,
    get_profile_photos_ds_app,
    update_person_flag,
)
from core.clients.ds_app import api as ds_app_api
from core.rules.person.utils.interests_utils import build_fb_pages_photo_text_list_for_weapons
from core.rules.person.utils.posts_utils import build_post_photo_text_list_for_weapons
from core.utils import build_person_urn


class WeaponsActions(PersonBaseActions):

    @rule_action()
    def set_person_weapons_extremism(self):
        posts_with_weapons = []
        pages_with_weapons = []
        photos_with_weapons = []
        cover_photos_with_weapons = []
        sub_categories: List[FlagSubCategory] = []
        try:
            try:
                posts_list = build_post_photo_text_list_for_weapons(
                    self.person.posts)
                ds_body = get_weapons_res(posts_list['posts_list'], self)
                for i, item in enumerate(ds_body):
                    if item.get("weapons"):
                        weapons_post = posts_list['posts_detected'][i]
                        posts_with_weapons.append(weapons_post)
            except Exception:
                pass

            try:
                interests_list = build_fb_pages_photo_text_list_for_weapons(
                    self.person.interests.pages
                )
                ds_body = get_weapons_res(interests_list['pages_list'], self)
                for i, item in enumerate(ds_body):
                    if item.get("weapons"):
                        weapons_page = interests_list['pages_detected'][i]
                        pages_with_weapons.append(weapons_page)
            except Exception:
                pass

            try:
                if person_images := self.person.personal_details.visuals:
                    cover_photos = get_cover_photos_ds_app(person_images)
                    if cover_photos:
                        ds_body = get_weapons_res(cover_photos, self)
                        for i, item in enumerate(ds_body):
                            if item.get("weapons"):
                                cover_photo = cover_photos[i]
                                cover_photos_with_weapons.append(cover_photo)
                    profile_photos = get_profile_photos_ds_app(person_images)
                    if profile_photos:
                        ds_body = get_weapons_res(profile_photos, self)
                        for item in ds_body:
                            if item.get("weapons"):
                                photo_key = item.get("hash")
                                profile_photo = (
                                    person_images.profile_photo.model_dump().get(
                                        photo_key
                                    )
                                )
                                photos_with_weapons.append(profile_photo)
            except Exception:
                pass

            all_lists = [
                posts_with_weapons,
                pages_with_weapons,
                photos_with_weapons,
                cover_photos_with_weapons,
            ]

            if any(all_lists):
                score = 0
                images_count = sum(len(lst) for lst in all_lists)
                if images_count == 1 or images_count == 2:
                    score += 4
                elif images_count == 3:
                    score += 5
                elif images_count >= 4:
                    score += 6
                if photos_with_weapons:
                    score += 2
                if cover_photos_with_weapons:
                    score += 2

                if photos_with_weapons or cover_photos_with_weapons or posts_with_weapons or pages_with_weapons:
                    sub_category = FlagSubCategory(
                        sub_category="Weapon Imagery",
                        severity=0.02,
                        description="Images contain weapon imagery. Prominent display may indicate potential risk or violent behavioral patterns.",
                        factors=[],
                    )
                    for photo in photos_with_weapons:
                        factor_data = Factor(
                            field="avatar",
                            source=FactorSource(
                                insight=(
                                    "Person has profile photos in social media that show weapons"
                                ),
                                photo=photo,
                            ),
                            ratio=1,
                        )
                        sub_category.factors.append(factor_data)
                    for photo in cover_photos_with_weapons:
                        factor_data = Factor(
                            field="cover",
                            source=FactorSource(
                                insight=(
                                    "Person has cover images in social media that show weapons"
                                ),
                                photo=photo["source"],
                            ),
                            ratio=1,
                        )
                        sub_category.factors.append(factor_data)
                    for post in posts_with_weapons:
                        factor_data = Factor(
                            field="post",
                            platform=(
                                "facebook"
                                if post.fb_post_text or post.fb_post_photo
                                else (
                                    "instagram"
                                    if post.instagram_post_text  # noqa
                                    else ("linkedin" if post.linkedin_post_text else "")
                                )
                            ),
                            source=FactorSource(
                                insight=(
                                    "Person has posts in social media that show weapons"
                                ),
                                text=(
                                    post.fb_post_text
                                    if post.fb_post_text
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
                                photo=(
                                    post.fb_post_photo.fb_photo.url
                                    if post.fb_post_photo  # noqa
                                    else (
                                        post.instagram_post_photo
                                        if post.instagram_post_photo  # noqa
                                        else (
                                            post.fb_uploaded_photo.fb_photo.url
                                            if post.fb_uploaded_photo  # noqa
                                            else (
                                                post.linkedin_post_photo
                                                if post.linkedin_post_photo
                                                else None
                                            )
                                        )
                                    )
                                ),
                                date=(
                                    datetime.utcfromtimestamp(
                                        post.fb_post_publish_at_date
                                    )
                                    if post.fb_post_publish_at_date
                                    else None
                                ),
                                url=(
                                    post.fb_post_url
                                    if post.fb_post_url
                                    else (
                                        post.linkedin_post_url
                                        if post.linkedin_post_url
                                        else None
                                    )
                                ),  # noqa
                            ),
                            ratio=1,
                        )
                        sub_category.factors.append(factor_data)
                    for page in pages_with_weapons:
                        factor_data = Factor(
                            field="page",
                            platform="facebook",
                            source=FactorSource(
                                insight=(
                                    "Person has pages in social media that show weapons"
                                ),
                                photo=page.fb_page_profile_photo,
                                url=page.fb_page_url,
                                text=page.fb_page_name,
                            ),
                            ratio=1,
                        )
                        sub_category.factors.append(factor_data)
                    sub_categories.append(sub_category)
                for sub_cat in sub_categories:
                    severity = float(score / len(sub_categories))
                    sub_cat.severity = severity

                self.flag.weapons = update_person_flag(
                    self.flag.weapons,
                    sub_categories=sub_categories,
                    category="Weapons",
                    description="Weapon imagery detected. Prominent display may indicate potential risk or violent behavioral patterns",
                    sub_category_to_delete="Weapon Imagery",
                )

        except Exception:
            pass


def get_weapons_res(req_list, self):
    ds_response = ds_app_api.ds_request.check_weapons(
        body=req_list, headers={
            "x-remote-context": build_person_urn(self.person.id)}
    )
    return ds_response.body
