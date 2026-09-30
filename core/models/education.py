from typing import Optional, List, Any, Union
from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from core.fields import S3Path, s3path_serializer

from .base import WithVerifiedFieldSchema
from .duration import Duration
from .period import Period


class LinkedinSchool(WithVerifiedFieldSchema):
    school_name: str = Field(..., examples=["Harvard"])
    degree_name: Optional[str] = Field(None, examples=["Engineering"])
    description: Optional[str] = Field(
        None, examples=["Engineering course..."])
    education_field: Optional[str] = Field(None, examples=["Phisics"])
    period: Optional[Period] = None
    duration: Optional[Duration] = None
    activities: Optional[List[Any]] = None
    school_logo_url: Optional[Union[AnyHttpUrl, S3Path]] = None
    school_url: Optional[AnyHttpUrl] = None
    linkedin_school_location: Optional[str] = Field(
        None, examples=["Boston, MA, USA"])

    @field_serializer("school_logo_url", when_used="json-unless-none")
    def serialize_school_logo_url_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class FacebookSchool(WithVerifiedFieldSchema):
    fb_school_name:  str = Field(..., examples=["Harvard"])
    fb_school_url: Optional[AnyHttpUrl] = None
    fb_school_description:  Optional[str] = Field(
        None, examples=["Business School"])
    fb_school_photo: Optional[Union[AnyHttpUrl, S3Path]] = None
    period: Optional[Period] = None
    fb_school_location: Optional[str] = Field(
        None, examples=["Boston, MA, USA"])
    fb_education_field: Optional[str] = Field(None, examples=["Archeology"])

    # validators
    @field_serializer("fb_school_photo", when_used="json-unless-none")
    def serialize_fb_school_photo_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class XingSchool(LinkedinSchool):
    degree_type: Optional[str] = Field(None, example="Master's degree")


class SchoolVariant(WithVerifiedFieldSchema):
    school_name: str = Field(..., examples=["Harvard"])
    degree_name: Optional[str] = Field(None, examples=["Engineering"])
    description: Optional[str] = Field(
        None, examples=["Engineering course..."])
    education_field: Optional[str] = Field(None, examples=["Phisics"])
    period: Optional[Period] = None
    duration: Optional[Duration] = None
    activities: Optional[List[Any]] = None
    school_logo_url: Optional[Union[AnyHttpUrl, S3Path]] = None
    school_url: Optional[AnyHttpUrl] = None
    school_location: Optional[str] = Field(
        None, examples=["Boston, MA, USA"])
    degree_type: Optional[str] = Field(None, example="Master's degree")
    school_photo: Optional[Union[AnyHttpUrl, S3Path]] = None


class Education(WithVerifiedFieldSchema):
    linkedin_schools: Optional[List[LinkedinSchool]] = None
    facebook_schools: Optional[List[FacebookSchool]] = None
    xing_schools: Optional[List[XingSchool]] = None
    school_variants: Optional[List[SchoolVariant]] = None
