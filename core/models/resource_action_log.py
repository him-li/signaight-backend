from beanie import TimeSeriesConfig, Granularity
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from .base import SignAIghtSchema, Document


class ResourceActionMeta(BaseModel):
    user_id: UUID
    kind: str
    action: str
    object_id: Optional[str] = None


class ResourceActionLog(SignAIghtSchema):
    ts: datetime = Field(default_factory=datetime.now)
    meta: ResourceActionMeta


class ResourceActionLogModel(ResourceActionLog, Document):

    class Settings:
        name = "resource_action_log"
        use_revision = False
        timeseries = TimeSeriesConfig(
            time_field="ts",
            meta_field="meta",
            granularity=Granularity.hours,
            expire_after_seconds=86400
        )
