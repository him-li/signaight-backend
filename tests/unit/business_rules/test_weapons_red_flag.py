import pytest

from core.models import FlagModel
from tests.unit.business_rules.test_business_rules import build_person_run_rules
from .rules import *
from .profiles import *


def getattr_or_key(obj, name, default=None):
    if hasattr(obj, name):
        return getattr(obj, name)
    if isinstance(obj, dict):
        return obj.get(name, default)
    return default


def has_post_photo(f, key):
    src = getattr_or_key(f, "source")
    photo = getattr(src, key, None) if src is not None else None
    return photo not in (None, "")


@pytest.mark.anyio
async def test_show_sample_images_that_clearly_depict_weaponry(
    person, editor, weapons_extremism_rules, profile_post_weapons
):
    person = await build_person_run_rules(
        person, editor, profile_post_weapons, weapons_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.weapons
    weapons_entry = next(
        (
            entry
            for entry in flag.weapons.sub_categories
            if entry.sub_category == "Weapon Imagery"
        ),
        None,
    )
    assert (
        weapons_entry is not None
    ), "No entry with sub_category='Weapon Imagery' found"
    assert len(weapons_entry.factors) == 3
    assert any(
        has_post_photo(factor, "photo") for factor in weapons_entry.factors
    )


@pytest.mark.anyio
async def test_show_sample_images_that_clearly_depict_weaponry_in_pages(
    person, editor, weapons_extremism_rules, profile_fb_page_weapon_profile_photo
):
    person = await build_person_run_rules(
        person, editor, profile_fb_page_weapon_profile_photo, weapons_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.weapons
    weapons_entry = next(
        (
            entry
            for entry in flag.weapons.sub_categories
            if entry.sub_category == "Weapon Imagery"
        ),
        None,
    )
    assert (
        weapons_entry is not None
    ), "No entry with sub_category='Weapon Imagery' found"
    assert len(weapons_entry.factors) == 1
    assert any(
        has_post_photo(factor, "photo")
        for factor in weapons_entry.factors
    )


@pytest.mark.anyio
async def test_show_sample_images_that_clearly_depict_weaponry_in_cover_photos(
    person, editor, weapons_extremism_rules, profile_with_cover_weapons
):
    person = await build_person_run_rules(
        person, editor, profile_with_cover_weapons, weapons_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.weapons
    weapons_entry = next(
        (
            entry
            for entry in flag.weapons.sub_categories
            if entry.sub_category == "Weapon Imagery"
        ),
        None,
    )
    assert (
        weapons_entry is not None
    ), "No entry with sub_category='Weapon Imagery' found"
    assert len(weapons_entry.factors) == 1
    assert any(
        has_post_photo(factor, "photo") for factor in weapons_entry.factors
    )


@pytest.mark.anyio
async def test_show_sample_images_that_clearly_depict_weaponry_in_profile_photos(
    person, editor, weapons_extremism_rules, profile_with_profile_picture_weapons
):
    person = await build_person_run_rules(
        person, editor, profile_with_profile_picture_weapons, weapons_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)

    assert flag.weapons
    weapons_entry = next(
        (
            entry
            for entry in flag.weapons.sub_categories
            if entry.sub_category == "Weapon Imagery"
        ),
        None,
    )
    assert (
        weapons_entry is not None
    ), "No entry with sub_category='Weapon Imagery' found"
    assert len(weapons_entry.factors) == 1
    assert any(
        has_post_photo(factor, "photo") for factor in weapons_entry.factors
    )


@pytest.fixture
def get_full_weapons_images(profile_with_profile_picture_weapons, profile_post_weapons, profile_fb_page_weapon_profile_photo):
    return {**profile_with_profile_picture_weapons, **profile_post_weapons, **profile_fb_page_weapon_profile_photo}


@pytest.mark.anyio
async def test_weapons_score(
    person, editor, weapons_extremism_rules, get_full_weapons_images
):
    person = await build_person_run_rules(
        person, editor, get_full_weapons_images, weapons_extremism_rules
    )
    flag = await FlagModel.find_one(FlagModel.person.id == person.id)
    # posts - 3, pages - 1, profile photo - 1. All photos = 5. Score = 6. Profile photo score = 2. Summ = 6 + 2
    assert flag.weapons.severity == 8
