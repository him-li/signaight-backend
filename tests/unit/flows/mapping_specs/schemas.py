from typing import Optional

from api.v1.persons.schemas import PersonalDetailsUpdate, NameOptional
from core.models.name import FullName


class OptionalFullName(FullName):
    full_name: Optional[str] = None


class OptionalName(NameOptional):
    full_name: Optional[OptionalFullName] = None


class PersonalDetailsTest(PersonalDetailsUpdate):
    name: Optional[OptionalName] = None
