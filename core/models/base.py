import uuid
from beanie import (
    Document as BaseDocument,
    Replace,
    Update,
    SaveChanges,
    ValidateOnSave,
    before_event
)
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional

from core.fields import S3Path

BaseModel.model_config["json_encoders"] = {
    S3Path: lambda v: str(v)
}


class SignAIghtSchema(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            S3Path: lambda v: str(v)
        }
    )


class WithVerifiedFieldSchema(SignAIghtSchema):
    verified: bool = Field(default=False, help="Verified info")


class DocumentEditorUser(SignAIghtSchema):
    id: uuid.UUID
    email: str
    firstname: str = "SignAIght"
    lastname: str = "SignAIght"


class UUIDModel(SignAIghtSchema):
    # NOTE: alias has been added to make OpenAPI schema compatible
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    id: uuid.UUID


class Document(UUIDModel, BaseDocument):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    pass


class Variant(SignAIghtSchema):
    source: Optional[str] = None
    value: str


class CreateUpdateMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now,
        examples=[str(datetime.now().isoformat())])
    updated_at: Optional[datetime] = Field(None,
        examples=[str(datetime.now().isoformat())])

    @before_event(Replace, Update, SaveChanges, ValidateOnSave)
    async def touch_updated_at(self):
        if hasattr(self, 'updated_at'):
            self.updated_at = datetime.now()
