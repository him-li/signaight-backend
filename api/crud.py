import abc
from typing import Dict, Optional, Union

from beanie.odm.queries.find import FindQuery
from fastapi import HTTPException, status

from api.acl import Principal
from api.local_authorization import (
    require_active_user, require_person_creation, require_project_access,
)
from core.models import UUIDModel


class CRUD(abc.ABC):
    principal: Principal
    kind = "api"

    def __init__(self, principal: Principal):
        self.principal = principal

    def get_principal(self) -> Principal:
        return self.principal

    @staticmethod
    def _deny(message: str = "Unauthorized access") -> None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

    async def authorized(
        self,
        action: str,
        context: Union[UUIDModel, FindQuery, Dict[str, object], None] = None,
        attr_map: Dict[str, str] | None = None,
        kind: Optional[str] = None,
        error_msg: str = "Unauthorized access",
    ):
        """Apply project ownership and person creation limits locally."""
        require_active_user(self.principal)
        if self.principal.is_admin:
            return context if isinstance(context, FindQuery) else True

        resource_kind = kind or self.kind
        if isinstance(context, FindQuery):
            if resource_kind != "api.v1.projects":
                self._deny(error_msg)
            from core.models import ProjectModel
            return context.find(ProjectModel.user_id == self.principal.id)

        if isinstance(context, dict):
            owner_id = context.get("owner_id") or context.get("user_id")
            future_count = context.get("future_persons_daily")
            if owner_id is None:
                self._deny(error_msg)
            if future_count is not None:
                require_person_creation(self.principal, owner_id, int(future_count))
            else:
                require_project_access(self.principal, owner_id)
            return True

        if action == "create" and resource_kind == "api.v1.projects":
            return True
        self._deny(error_msg)


class ReadCRUD(CRUD):
    @abc.abstractmethod
    async def list(self): ...
    @abc.abstractmethod
    async def read(self, id): ...


class CreateCRUD(CRUD):
    @abc.abstractmethod
    async def create(self): ...


class UpdateCRUD(CRUD):
    @abc.abstractmethod
    async def update(self, id, data): ...


class DeleteCRUD(CRUD):
    @abc.abstractmethod
    async def delete(self, id): ...


class BasicCRUD(CreateCRUD, ReadCRUD, UpdateCRUD, DeleteCRUD):
    pass
