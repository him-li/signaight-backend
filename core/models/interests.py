from typing import Any, Optional, List, Union
from pydantic import AnyHttpUrl, field_serializer
from datetime import datetime
from core.fields import S3Path, s3path_serializer

from .base import WithVerifiedFieldSchema, SignAIghtSchema, Variant


class Page(WithVerifiedFieldSchema):
    fb_page_name: Optional[str] = None
    fb_page_profile_photo: Optional[Union[AnyHttpUrl, S3Path]] = None
    fb_page_cover_photo: Optional[Union[AnyHttpUrl, S3Path]] = None
    fb_page_url: Optional[AnyHttpUrl] = None
    fb_page_id: Optional[str] = None

    @field_serializer(
        "fb_page_profile_photo", "fb_page_cover_photo", when_used="json-unless-none"
    )
    def serialize_fb_page_photos_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class LinkedinInfluencers(SignAIghtSchema):
    linkedin_full_name: Optional[str] = None
    linkedin_headline: Optional[str] = None
    linkedin_followers_count: Optional[int] = None
    linkedin_profile_url: Optional[AnyHttpUrl] = None
    linkedin_profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    linkedin_is_influencer: Optional[bool] = None

    @field_serializer("linkedin_profile_picture", when_used="json-unless-none")
    def serialize_linkedin_profile_picture_s3path(self,
                                                  v: S3Path | str | None,
                                                  info):
        return s3path_serializer(v, info)


class LinkedinInterests(LinkedinInfluencers):
    pass


class TelegramMessage(SignAIghtSchema):
    date: Optional[str] = None
    media_code: Optional[Any] = None
    media_name: Optional[Any] = None
    message_id: Optional[int] = None
    reply_to_message_id: Optional[int] = None
    text: Optional[str] = None


class TelegramGroup(SignAIghtSchema):
    telegram_public_group_id: Optional[str] = None
    telegram_public_group_screen_name: Optional[str] = None
    title: Optional[str] = None
    lastseen: Optional[datetime] = None
    messages: Optional[List[TelegramMessage]] = None


class Groups(SignAIghtSchema):
    telegram_groups: Optional[List[TelegramGroup]] = None


class Interests(WithVerifiedFieldSchema):
    pages: Optional[List[Page]] = None
    followed_hashtags: Optional[Any] = None
    groups: Optional[Groups] = None
    linkedin_interests: Optional[List[LinkedinInterests]] = None
    xing_interests: Optional[List[str]] = None
    interest_variants: Optional[List[Variant]] = None
