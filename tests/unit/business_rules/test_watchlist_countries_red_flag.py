import pytest
import re

from core.models import FlagModel
from tests.unit.business_rules.test_business_rules import build_person_run_rules
from .rules import *
from .profiles import *

@pytest.mark.anyio
async def test_profile_location_in_watchlist_country(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_in_watchlist_country_without_twitter
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_in_watchlist_country_without_twitter,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    assert flags.watchlist_countries

@pytest.mark.skip(reason="This test works locally but fails in CI, needs investigation")
@pytest.mark.anyio
async def test_profile_location_in_watchlist_country_alpha_2(
    person,
    editor,
    watchlist_countries_rules,
    profile_location_in_watchlist_country_without_twitter
):
    person = await build_person_run_rules(
        person, editor,
        profile_location_in_watchlist_country_without_twitter,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    countries_str = flags.watchlist_countries.description
    
    assert re.search(r"\bBD\b", countries_str)
    assert re.search(r"\bIN\b", countries_str)
    
@pytest.mark.anyio
async def test_geo_trace_grouping(
    person,
    editor,
    watchlist_countries_rules,
    geo_trace_grouping
):
    person = await build_person_run_rules(
        person, editor,
        geo_trace_grouping,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    countries_str = flags.watchlist_countries.description
    assert re.search(r"\bBD\b", countries_str)
    assert re.search(r"\bIN\b", countries_str)

@pytest.mark.anyio
async def test_profile_location_in_watchlist_country_geo_trace(
    person,
    editor,
    watchlist_countries_rules,
    geo_trace_with_watchlist_country
):
    person = await build_person_run_rules(
        person, editor,
        geo_trace_with_watchlist_country,
        watchlist_countries_rules)
    flags = await FlagModel.find_one(
        FlagModel.person.id == person.id)
    countries_str = flags.watchlist_countries.description
    assert re.search(r"\bIR\b", countries_str)
    assert re.search(r"\bID\b", countries_str)
    assert flags.watchlist_countries
    assert flags.watchlist_countries.severity == 10
    
