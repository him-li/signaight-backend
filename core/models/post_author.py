from datetime import date, datetime
from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema
from .twitter_description import TwitterDescription


class FacebookPostAuthor(SignAIghtSchema):
    fb_full_name: Optional[str] = Field(None, examples=["John Doe"])
    fb_user_id: Optional[str] = Field(None, help="Post author's facebook id")
    fb_gender: Optional[str] = Field(
        None, help="Post author's facebook gender")
    fb_profile_url: Optional[AnyHttpUrl] = None


class LinkedinPostAuthor(SignAIghtSchema):
    linkedin_f_name: Optional[str] = Field(
        None, help="Post author's Linkedin first_name")
    linkedin_l_name: Optional[str] = Field(
        None, help="Post author's Linkedin last_name")
    title: Optional[str] = Field(None, help="Post author's Linkedin title")
    linkedin_profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    linkedin_profile_url: Optional[AnyHttpUrl] = None

    # serializers
    @field_serializer("linkedin_profile_picture", when_used="json-unless-none")
    def serialize_linkedin_profile_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class TwitterPostAuthor(SignAIghtSchema):
    twitter_user_id: Optional[str] = None
    twitter_created_at: Optional[Union[str, date, datetime]] = None
    twitter_full_name: Optional[str] = None
    twitter_username: Optional[str] = None
    twitter_location: Optional[str] = None
    twitter_favourites_count: Optional[int] = None
    twitter_followers_count: Optional[int] = None
    twitter_following_count: Optional[int] = None
    twitter_media_count: Optional[int] = None
    twitter_cover_photo: Optional[Union[S3Path, AnyHttpUrl]] = None
    twitter_profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    twitter_is_protected: Optional[bool] = None
    twitter_statuses_count: Optional[int] = None
    twitter_description: Optional[TwitterDescription] = None

    # serializers
    @field_serializer(
        'twitter_cover_photo',
        'twitter_profile_picture'
    )
    def serialize_twitter_cover_or_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class PostAuthor(FacebookPostAuthor, LinkedinPostAuthor, TwitterPostAuthor):
    pass
