from datetime import datetime
from types import SimpleNamespace

from core.providers import build_fixture_candidates


def _person():
    return SimpleNamespace(personal_details=SimpleNamespace(name=SimpleNamespace(
        first_name=SimpleNamespace(f_name="Ada"),
        last_name=SimpleNamespace(l_name="Lovelace"))))


def test_fixture_provider_returns_normalized_candidates():
    timestamp = datetime(2026, 1, 2, 3, 4, 5)
    candidates = build_fixture_candidates(_person(), "search-1", timestamp)
    assert len(candidates) == 6
    assert {item["source"] for item in candidates} == {
        "linkedin", "instagram", "facebook"}
    assert all(item["resource"] == "fixture" for item in candidates)
    assert all(item["primary"] is False for item in candidates)


def test_fixture_provider_is_deterministic_and_uses_person_name():
    timestamp = datetime(2026, 1, 2, 3, 4, 5)
    first = build_fixture_candidates(_person(), "search-1", timestamp)
    assert first == build_fixture_candidates(_person(), "search-1", timestamp)
    assert first[0]["personal_details"]["name"]["full_name"][
        "linkedin_full_name"] == "Ada Lovelace"
    assert first[0]["network_signature"]["username"][
        "linkedin_username"] == ["ada.lovelace"]
