from typing import Optional, List

from .base import SignAIghtSchema, WithVerifiedFieldSchema
from .volunteering_experience import VolunteeringExperience
from .causes import Cause
from .certification import Certification


class LinkedinVolunteeringExperiences(SignAIghtSchema):
    certificates: Optional[str] = None


class VolunteerExperience(WithVerifiedFieldSchema):
    volunteer_experience: Optional[List[VolunteeringExperience]] = None
    linkedin_volunteering_experiences: Optional[
        LinkedinVolunteeringExperiences] = None
    certificates: Optional[List[Certification]] = None
    role: Optional[List] = None
    cause: Optional[List[Cause]] = None
