from typing import Optional, List, Any, Union
from pydantic import (
    Field,
    AnyHttpUrl,
    field_serializer
)
from core.fields import S3Path, s3path_serializer

from .base import WithVerifiedFieldSchema
from .position import Position
from .project_part_of import ProjectPartOf
from .honor import Honor
from .publication import Publication
from .organization import Organization
from .course import Course
from .skill import Skill
from .period import Period
from .recommendation import Recommendation
from .licence_certification import LicenceCertification
from .volunteering_experience import VolunteeringExperience


class LinkedinWork(WithVerifiedFieldSchema):
    positions: Optional[List[Position]] = None
    linkedin_endorsement: Optional[List[Any]] = None
    projects: Optional[List[ProjectPartOf]] = None
    honors: Optional[List[Honor]] = None
    publications: Optional[List[Publication]] = None
    organizations: Optional[List[Organization]] = None
    courses: Optional[List[Course]] = None
    skills: Optional[List[Skill]] = None
    recommendations: Optional[List[Recommendation]] = None
    licences_certifications: Optional[List[LicenceCertification]] = None
    volunteering_experiences: Optional[List[VolunteeringExperience]] = None


class FacebookWork(WithVerifiedFieldSchema):
    fb_workplace_name: str = Field(..., examples=["Nasa"])
    fb_workplace_url: Optional[AnyHttpUrl] = None
    fb_work_title: Optional[str] = Field(None, examples=["Senior Engineer"])
    fb_work_description: Optional[str] = Field(
        None, examples=["Senior Engineer in dept"])
    fb_workplace_photo_url: Optional[Union[AnyHttpUrl, S3Path]] = None
    fb_work_period: Optional[Period] = None
    fb_field: Optional[str] = Field(None, examples=["Aerospatial engineering"])
    fb_workplace_location: Optional[str] = Field(
        None, examples=["Houston, TX"])

    @field_serializer("fb_workplace_photo_url", when_used="json-unless-none")
    def serialize_fb_workplace_photo_url_s3path(
            self,
            v: S3Path | str | None,
            info):
        return s3path_serializer(v, info)


class XingSkills(WithVerifiedFieldSchema):
    top_skills: Optional[List[Skill]] = None
    hard_skills: Optional[List[Skill]] = None
    soft_skills: Optional[List[Skill]] = None


class XingQualification(WithVerifiedFieldSchema):
    issue_date: Optional[str] = None
    name: Optional[str] = None
    qualification_url: Optional[AnyHttpUrl] = None


class XingWork(WithVerifiedFieldSchema):
    positions: Optional[List[Position]] = None
    skills: Optional[XingSkills] = None
    qualifications_achievements: Optional[List[XingQualification]] = None


class Qualification(WithVerifiedFieldSchema):
    issue_date: Optional[str] = None
    name: Optional[str] = None
    qualification_url: Optional[AnyHttpUrl] = None


class CareerVariants(WithVerifiedFieldSchema):
    positions: Optional[List[Position]] = None
    endorsements: Optional[List[Any]] = None
    projects: Optional[List[ProjectPartOf]] = None
    honors: Optional[List[Honor]] = None
    publications: Optional[List[Publication]] = None
    organizations: Optional[List[Organization]] = None
    courses: Optional[List[Course]] = None
    skills: Optional[List[Skill]] = None
    recommendations: Optional[List[Recommendation]] = None
    licences_certifications: Optional[List[LicenceCertification]] = None
    volunteering_experiences: Optional[List[VolunteeringExperience]] = None
    qualifications_achievements: Optional[List[Qualification]] = None


class Work(WithVerifiedFieldSchema):
    linkedin_work: Optional[LinkedinWork] = None
    facebook_work: Optional[List[FacebookWork]] = None
    xing_work: Optional[XingWork] = None
    # TODO: remove alias after successful testing with new field names
    career_variants: Optional[CareerVariants] = Field(
        None, alias="work_variants")
