import importlib
import uuid
from beanie import (
    UnionDoc,
    before_event,
    after_event,
    Insert,
    Replace,
    Update,
    SaveChanges,
    ValidateOnSave
)
from enum import Enum
from datetime import datetime
from flatten_json import unflatten_list
from pydantic import field_validator, Field
from pymongo import IndexModel, ASCENDING
from typing import Optional

from core.exceptions import DocumentCouldNotBeSaved

from .base import SignAIghtSchema, DocumentEditorUser


class UnionAuditLog(UnionDoc):

    class Settings:
        name = "audit_logs"
        class_id = "_class_id"

# NOTE: to allow records made by system we need make
# remote user id and email optional


class AuditLogUser(DocumentEditorUser):
    id: Optional[uuid.UUID] = None
    email: Optional[str] = None


class ActionsEnum(str, Enum):
    insert = 'Insert'
    update = 'Update'
    replace = 'Replace'
    save_changes = 'SaveChanges'


class AuditLog(SignAIghtSchema):
    editor: AuditLogUser
    revision_id: uuid.UUID
    action: ActionsEnum
    changes: dict
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now, examples=[
            str(datetime.now().isoformat())]
    )


class AuditLogMixin():
    """Require to use audit log mixin

        class SomeModel(AuditLogMixin, Document, Some):

            class Settings:
                use_state_management = True
                state_management_save_previous = True
                use_revision = True
    """

    last_edited_by: AuditLogUser

    @before_event(Insert, Replace, Update, SaveChanges, ValidateOnSave)
    async def check_editor_info(self):
        if not self.last_edited_by:
            raise DocumentCouldNotBeSaved(
                "Can not save audit log without user info. "
                "Set info using last_edited_by model attribute or the set_editor method.")  # noqa

    @field_validator('last_edited_by')
    @classmethod
    def document_must_contain_editor_info(cls, v):
        # maybe add to check not isinstance(v, AuditLogUser)
        if not v:
            # by default it should be SignAIght SignAIght
            v = AuditLogUser()
        return v

    def set_editor(self,
                   id: str | uuid.UUID | None,
                   email: str | None,
                   firstname: str = "",
                   lastname: str = ""):
        """
        Example of setting editor data:
        instance.set_editor(
            id=editor_user_id,
            email=editor_email,
            firstname=editor_first_name,
            lastname=editor_last_name
        )
        """

        self.last_edited_by = AuditLogUser(
            id=id,
            email=email,
            firstname=firstname,
            lastname=lastname,
        )

    def get_editor(self):
        return self.last_edited_by

    @after_event(Insert)
    async def log_after_entity_insert(self):
        await self._log_changes("Insert", self.model_dump())

    @after_event(SaveChanges)
    async def log_after_entity_savechanges(self):
        changes = self.get_previous_changes()
        try:
            if changes and isinstance(changes, dict):
                changes = unflatten_list(changes, ".")
        except Exception as e:
            print(str(e))
        # TODO: save all results even in flatten form except empty
        await self._log_changes("SaveChanges", changes)

    @after_event(Replace)
    async def log_after_entity_replace(self):
        await self._log_changes("Replace", self.model_dump())

    async def _log_changes(self, action, changes):
        # NOTE: ommit empty changes as parasite records
        if not changes:
            return
        data = {
            "entity": self.id,
            "editor": self.get_editor(),
            "revision_id": self.revision_id,
            "action": action,
            "changes": changes
        }
        class_name = f"{self.__class__.__name__}AuditLog"
        try:
            AuditLogClass = getattr(importlib.import_module("core.models"),
                                    class_name)
            audit_log = AuditLogClass(**data)
            await audit_log.insert()
        except Exception as e:
            print(str(e))
            return
