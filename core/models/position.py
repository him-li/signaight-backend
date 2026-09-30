from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema
from .period import Period
from .duration import Duration


class Position(SignAIghtSchema):
    title: Optional[str] = Field(None, examples=["Senior Engineer"])
    employment_type: Optional[str] = Field(None, examples=["Full_time"])
    description: Optional[str] = Field(
        None, examples=["Worked as Senior Engineer..."])
    company_name: Optional[str] = Field(None, examples=["Nasa"])
    company_public_identifier: Optional[str] = None
    company_logo_url: Optional[Union[AnyHttpUrl, S3Path]] = None
    location: Optional[str] = Field(None, examples=["Denver"])
    company_website: Optional[AnyHttpUrl] = None
    country: Optional[str] = None
    linkedin_company_url: Optional[AnyHttpUrl] = None
    xing_company_url: Optional[AnyHttpUrl] = None
    linkedin_industry: Optional[str] = Field(None, examples=["Software"])
    company_industry: Optional[str] = Field(None, examples=["Software"])
    company_number_of_employees: Optional[str] = Field(None, examples=["100"])
    period: Optional[Period] = None
    duration: Optional[Duration] = None

    @field_serializer("company_logo_url", when_used="json-unless-none")
    def serialize_company_logo_url_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)

    @field_serializer(
        "linkedin_company_url", "xing_company_url", when_used="json-unless-none"
    )
    def serialize_company_urls(self, v: AnyHttpUrl | str | None, info):
        if v:
            try:
                return AnyHttpUrl(v)
            except Exception:
                return None
