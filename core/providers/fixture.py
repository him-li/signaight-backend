"""Deterministic offline candidates using the live provider data shape."""

from datetime import datetime
from typing import Any


def _name_parts(person: Any) -> tuple[str, str]:
    name = getattr(getattr(person, "personal_details", None), "name", None)
    first = getattr(getattr(name, "first_name", None), "f_name", None)
    last = getattr(getattr(name, "last_name", None), "l_name", None)
    return first or "Alex", last or "Morgan"


def _candidate(*, first: str, last: str, source: str, variant: int,
               search_id: str, searched_at: datetime) -> dict[str, Any]:
    suffix = "" if variant == 1 else str(variant)
    username = f"{first}.{last}{suffix}".lower().replace(" ", "")
    full_name = f"{first} {last}" + (f" {variant}" if variant > 1 else "")
    return {
        "search_id": search_id, "searched_at": searched_at,
        "source": source, "resource": "fixture", "primary": False,
        "similarity": 0.92 if variant == 1 else 0.61,
        "personal_details": {"name": {
            "first_name": {"f_name": first, f"{source}_f_name": first},
            "last_name": {"l_name": last, f"{source}_l_name": last},
            "full_name": {"full_name": full_name,
                          f"{source}_full_name": full_name}}},
        "network_signature": {
            "user_id": {f"{source}_user_id": [f"fixture-{source}-{username}"]},
            "username": {f"{source}_username": [username]},
            "url": {f"{source}_profile_url": [
                f"https://example.invalid/{source}/{username}"]}},
    }


def build_fixture_candidates(person: Any, search_id: str,
                             searched_at: datetime | None = None
                             ) -> list[dict[str, Any]]:
    """Return stable candidates that exercise review without network access."""
    first, last = _name_parts(person)
    timestamp = searched_at or datetime.now()
    return [_candidate(first=first, last=last, source=source, variant=variant,
                       search_id=search_id, searched_at=timestamp)
            for source in ("linkedin", "instagram", "facebook")
            for variant in (1, 2)]
