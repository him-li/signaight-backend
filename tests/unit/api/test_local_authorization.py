import pytest
from fastapi import HTTPException

from api.local_authorization import (
    Principal, require_active_user, require_person_creation,
    require_project_access,
)


def user(id="user-1", *, active=True, verified=True, admin=False):
    roles = frozenset({"signaight:admin"}) if admin else frozenset()
    return Principal(id, roles, active, verified)


def test_owner_can_create_person_within_daily_limit():
    require_person_creation(user(), "user-1", 10)


def test_other_project_owner_is_denied():
    with pytest.raises(HTTPException) as exc:
        require_project_access(user(), "user-2")
    assert exc.value.status_code == 403


def test_daily_limit_is_enforced():
    with pytest.raises(HTTPException) as exc:
        require_person_creation(user(), "user-1", 11)
    assert exc.value.status_code == 403


def test_admin_can_cross_project_boundary():
    require_person_creation(user("admin", admin=True), "user-2", 999)


@pytest.mark.parametrize("active,verified", [(False, True), (True, False)])
def test_inactive_user_is_denied(active, verified):
    with pytest.raises(HTTPException) as exc:
        require_active_user(user(active=active, verified=verified))
    assert exc.value.status_code == 403
