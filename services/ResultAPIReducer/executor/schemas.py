from typing import Optional
from core.models import (
    Person,
    BiographicDetails,
    NetworkSignature,
    PersonalDetails)
from core.models.name import Name
from core.models.email import Email


class PersonalDetailsUpdate(PersonalDetails):
    name: Optional[Name] = None
    email: Optional[Email] = None


class PersonUpdate(Person):
    biographic_details: Optional[BiographicDetails] = None
    network_signature: Optional[NetworkSignature] = None
    personal_details: Optional[PersonalDetailsUpdate] = None
