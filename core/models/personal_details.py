from typing import Optional

from .base import WithVerifiedFieldSchema
from .name import Name
from .phone import Phone
from .gender import Gender
from .visuals import Visuals
from .email import Email
from .birth_year_date import BirthYearBirthday
from .websites import Websites
from .languages import Languages
from .location import Location
from .additional_details import AdditionalDetails
from .nationality import Nationality


class PersonalDetails(WithVerifiedFieldSchema):
    name: Optional[Name] = None
    phone: Optional[Phone] = None
    gender: Optional[Gender] = None
    visuals: Optional[Visuals] = None
    email: Optional[Email] = None
    birth_year_birthday: Optional[BirthYearBirthday] = None
    websites: Optional[Websites] = None
    languages: Optional[Languages] = None
    location: Optional[Location] = None
    nationality: Optional[Nationality] = None
    additional_details: Optional[AdditionalDetails] = None
    ethnicity: Optional[str] = None
