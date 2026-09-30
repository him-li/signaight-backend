from core.utils.get_person_display_name import get_person_display_name
import pytest

from core.models import FlagModel, PersonModel
from .rules import *
from .profiles import *


@pytest.mark.anyio
async def test_get_person_display_name(profile_with_full_name, editor):
    person_data = {**profile_with_full_name, **editor}
    person = PersonModel(**person_data)
    display_name = get_person_display_name(person)

    assert display_name == "John Doe"


@pytest.mark.anyio
async def test_get_person_display_name_without_full_name(
    profile_without_full_name, editor
):
    person_data = {**profile_without_full_name, **editor}
    person = PersonModel(**person_data)
    display_name = get_person_display_name(person)

    assert display_name == "Johnatan Doe"


@pytest.mark.anyio
async def test_get_person_display_name_without_name(profile_without_name, editor):
    person_data = {**profile_without_name, **editor}
    person = PersonModel(**person_data)
    display_name = get_person_display_name(person)

    assert display_name == "No name"
