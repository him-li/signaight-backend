import pytest
from core.models import PersonModel
from tests.unit.business_rules.profiles import *  # noqa


@pytest.mark.anyio
async def test_update_geotrace(
        profile_with_check_ins,
        editor):
    person_data = {**profile_with_check_ins, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()
    assert person.geo_trace
    # NOTE: sometimes mapbox response with 14 features instead 15
    assert len(person.geo_trace.features) in [12, 13, 14, 15]
    for feature in person.geo_trace.features:
        assert feature.properties.location_type
        if not feature.properties.date:
            assert "check_in" not in feature.properties.location_type


@pytest.mark.anyio
async def test_update_geotrace_google_reviews(
        profile_with_google_reviews,
        editor):
    person_data = {**profile_with_google_reviews, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()
    assert person.geo_trace
    # NOTE: teorethiclally could same problem as in previous test
    assert len(person.geo_trace.features) == 5
    for feature in person.geo_trace.features:
        assert feature.properties.location_type
        if not feature.properties.date:
            assert "check_in" not in feature.properties.location_type


@pytest.mark.anyio
async def test_update_geotrace_no_duplicate_residence(
        profile_with_hometown_current_city_equal,
        editor):
    person_data = {**profile_with_hometown_current_city_equal, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()

    assert person.geo_trace
    assert len(person.geo_trace.features) == 2


@pytest.mark.anyio
async def test_update_geotrace_no_duplicate_residence_different_casing(
        profile_with_hometown_current_city_equal_different_casing,
        editor):
    person_data = {
        **profile_with_hometown_current_city_equal_different_casing, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()

    assert person.geo_trace
    assert len(person.geo_trace.features) == 2


@pytest.mark.anyio
async def test_update_geotrace_no_duplicate_residence_different_writing(
        profile_with_hometown_current_city_equal_different_writing,
        editor):
    person_data = {
        **profile_with_hometown_current_city_equal_different_writing, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()

    assert person.geo_trace
    # NOTE: teorethiclally could same problem as in previous test
    assert len(person.geo_trace.features) == 2


@pytest.mark.anyio
async def test_update_geotrace_profile_with_checkins_not_shown_in_geotrace(
        profile_with_checkins_not_shown_in_geotrace,
        editor):
    person_data = {
        **profile_with_checkins_not_shown_in_geotrace, **editor}
    person = PersonModel(**person_data)

    await person.create_person_geotrace()

    assert person.geo_trace
    for feature in person.geo_trace.features:
        if feature.properties.location_type == "check_ins":
            print(feature)
    assert len(person.geo_trace.features) == 4
