from typing import Optional

from .base import WithVerifiedFieldSchema
from .description_bio_intro import DescriptionBioIntro
from .volunteer_experience import VolunteerExperience
from .marital_status_relatives import MaritalStatusRelatives
from .education import Education
from .work import Work


class BiographicDetails(WithVerifiedFieldSchema):
    description_bio_intro: Optional[DescriptionBioIntro] = None
    volunteer_experience: Optional[VolunteerExperience] = None
    marital_status_relatives: Optional[MaritalStatusRelatives] = None
    education: Optional[Education] = None
    work: Optional[Work] = None
