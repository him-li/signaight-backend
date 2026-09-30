import datetime
from typing import Optional, List, Union
from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer,
    field_validator
)

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema, WithVerifiedFieldSchema, Variant


class FacebookRelative(SignAIghtSchema):
    fb_family_member_name: Optional[str] = Field(
        None, help="Family member's name")
    fb_family_member_type: Optional[str] = Field(None, examples=["son"])
    fb_family_member_relation_from: Optional[datetime.date] = Field(
        None, examples=["01/01/2000"])
    fb_user_id: Optional[str] = Field(None, help="Family member's facebook id")
    fb_profile_url: Optional[AnyHttpUrl] = Field(
        None, help="Family member's Facebook profile url")
    fb_username: Optional[str] = Field(
        None, help="Family member's Facebook username")
    fb_profile_page: Optional[AnyHttpUrl] = Field(
        None, help="Family member's profile page url")
    fb_profile_picture: Optional[Union[AnyHttpUrl, S3Path]] = Field(
        None, examples=["s3://media.signaight.ai/profile_pictures/images/82.jpg"])

    @field_serializer("fb_profile_picture", when_used="json-unless-none")
    def serialize_fb_profile_picture_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class FacebookMaritalStatus(SignAIghtSchema):
    fb_marital_status: Optional[str] = Field(None, examples=["married"])
    fb_partner: Optional[FacebookRelative] = None


class MaritalStatusRelatives(WithVerifiedFieldSchema):
    marital_status: Optional[str] = Field(None, examples=["married"])
    fb_marital_status: Optional[FacebookMaritalStatus] = None
    facebook_family_members: Optional[List[FacebookRelative]] = None
    marital_status_variants: Optional[Variant] = None
    family_members_variants: Optional[List[Variant]] = None

    @field_validator('fb_marital_status', mode='before')
    @classmethod
    def str_to_dict(cls, value: dict | str) -> FacebookMaritalStatus:
        # backward compatibility with old records as string
        if isinstance(value, str):
            value = FacebookMaritalStatus(fb_marital_status=value)
        return value
