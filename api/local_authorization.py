"""Small, testable authorization rules for the local-auth runtime."""

from dataclasses import dataclass, field

from fastapi import HTTPException

PERSON_DAILY_LIMIT = 10


@dataclass(frozen=True)
class Principal:
    id: str
    roles: frozenset[str] = field(default_factory=frozenset)
    is_active: bool = False
    email_verified: bool = False
    email: str | None = None
    first_name: str = ""
    last_name: str = ""

    @property
    def is_admin(self) -> bool:
        return "signaight.admin" in {
            role.replace(":", ".") for role in self.roles
        }


def require_active_user(principal: Principal) -> None:
    if not principal.is_active or not principal.email_verified:
        raise HTTPException(status_code=403, detail="Unauthorized access")


def require_project_access(principal: Principal, owner_id: object) -> None:
    require_active_user(principal)
    if not principal.is_admin and str(owner_id) != principal.id:
        raise HTTPException(status_code=403, detail="Project access denied")


def require_person_creation(
    principal: Principal, owner_id: object, future_daily_count: int,
) -> None:
    require_project_access(principal, owner_id)
    if not principal.is_admin and future_daily_count > PERSON_DAILY_LIMIT:
        raise HTTPException(
            status_code=403, detail="Daily person creation limit reached"
        )
