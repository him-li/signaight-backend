from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema


class FacebookTaggedPerson(SignAIghtSchema):
    fb_user_id: Optional[str] = Field(None, help="facebook id")
    fb_full_name: Optional[str] = Field(None, examples=["John Doe"])
    fb_profile_url: Optional[AnyHttpUrl] = None


class InstagramTaggedPerson(SignAIghtSchema):
    instagram_id: Optional[str] = Field(None, examples=["123456789"])
    instagram_username: Optional[str] = Field(None, examples=["johndoe"])
    instagram_full_name: Optional[str] = Field(None, examples=["John Doe"])
    instagram_is_private: Optional[bool] = Field(None, examples=[False])
    instagram_is_verified: Optional[bool] = Field(None, examples=[False])
    instagram_profile_picture: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"])

    @field_serializer("instagram_profile_picture", when_used="json-unless-none")
    def serialize_instagram_profile_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)

class LinkedinTaggedPerson(SignAIghtSchema):
    linkedin_f_name: Optional[str] = None
    linkedin_l_name: Optional[str] = None
    linkedin_headline: Optional[str] = None
    linkedin_profile_picture: Optional[Union[S3Path, AnyHttpUrl]] = None
    linkedin_profile_url: Optional[AnyHttpUrl] = None

    @field_serializer("linkedin_profile_picture", when_used="json-unless-none")
    def serialize_linkedin_profile_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class TwitterTaggedPerson(SignAIghtSchema):
    twitter_user_id: Optional[str] = None
    twitter_full_name: Optional[str] = None
    twitter_username: Optional[str] = None


class TaggedPerson(FacebookTaggedPerson,
                   InstagramTaggedPerson,
                   LinkedinTaggedPerson,
                   TwitterTaggedPerson):
    pass
