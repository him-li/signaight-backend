from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from typing import Optional, Union, List

from core.fields import S3Path, s3path_serializer

from .base import SignAIghtSchema, Document


class FoundedOn(SignAIghtSchema):
    month: Optional[int] = None
    year: Optional[int] = None
    day: Optional[int] = None


class CompanyLocation(SignAIghtSchema):
    country: Optional[str] = None
    geographic_area: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    headquarter: Optional[bool] = None


class EmployeeCountRange(SignAIghtSchema):
    start: Optional[int] = None
    end: Optional[int] = None


class ParentCompany(SignAIghtSchema):
    name: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
    urn: Optional[str] = None


class Company(SignAIghtSchema):
    name: Optional[str] = Field(None, examples=["Company Name"])
    linkedin_urn: Optional[str] = None
    universal_name: Optional[str] = None
    description: Optional[str] = None
    employee_count: Optional[int] = None
    employee_count_range: Optional[EmployeeCountRange] = None
    followers_count: Optional[int] = None
    founded_on: Optional[FoundedOn] = None
    phone: Optional[str] = None
    specialties: Optional[List[str]] = None
    linkedin_url: Optional[AnyHttpUrl] = None
    website_url: Optional[AnyHttpUrl] = None
    crunchbase_url: Optional[AnyHttpUrl] = None
    logo_url: Optional[Union[S3Path, AnyHttpUrl]] = None
    industry: Optional[str] = None
    locations: Optional[List[CompanyLocation]] = None
    organization_type: Optional[str] = None
    headline: Optional[str] = None
    public_identifier: Optional[str] = None
    parent_company: Optional[ParentCompany] = None

    @field_serializer("logo_url", when_used="json-unless-none")
    def serialize_logo_url_s3path(self, v: S3Path | str | None, info):
        return s3path_serializer(v, info)


class CompanyModel(Document, Company):

    class Settings:
        name = "companies"
        use_revision = False
