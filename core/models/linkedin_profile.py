from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema
from .position import Position
from .certification import Certification
from .course import Course
from .education import Education
from .honor import Honor
from .language import Language
from .organization import Organization
from .patent import Patent
from .phone_number import PhoneNumber
from .project_part_of import ProjectPartOf
from .publication import Publication
from .skill import Skill
from .test_score import TestScore
from .volunteering_experience import VolunteeringExperience
from .volunteering_interest import VolunteeringInterest
from .website import Website


class LinkedInProfile(SignAIghtSchema):
    linkedin_f_name: Optional[str] = Field(None, examples=["John"])
    linkedin_l_name: Optional[str] = Field(None, examples=["Doe"])
    linkedin_full_name: Optional[str] = Field(None, examples=["John Doe"])
    linkedin_username: Optional[str] = Field(None, examples=["johndoe"])
    linkedin_email_address: Optional[List] = None
    linkedin_id: Optional[str] = Field(None, examples=["123456789"])
    linkedin_profile_url: Optional[str] = Field(None, examples=["https://...."])
    linkedin_profile_picture: Optional[str] = Field(None, examples=["https://...."])
    linkedin_location: Optional[str] = Field(None, examples=["Los Angeles, CA"])
    linkedin_positions: Optional[List[Position]] = None
    linkedin_certifications: Optional[List[Certification]] = None
    linkedin_courses: Optional[List[Course]] = None
    linkedin_educations: Optional[List[Education]] = None
    linkedin_honors: Optional[List[Honor]] = None
    linkedin_languages: Optional[List[Language]] = None
    linkedin_organizations: Optional[List[Organization]] = None
    linkedin_patents: Optional[List[Patent]] = None
    linkedin_phone_numbers: Optional[List[PhoneNumber]] = None
    linkedin_projects_part_of: Optional[List[ProjectPartOf]] = None
    linkedin_publications: Optional[List[Publication]] = None
    linkedin_skills: Optional[List[Skill]] = None
    linkedin_test_scores: Optional[List[TestScore]] = None
    linkedin_volunteering_experiences: Optional[List[VolunteeringExperience]] = None
    linkedin_volunteering_interests: Optional[List[VolunteeringInterest]] = None
    linkedin_websites: Optional[List[Website]] = None
