from beanie import TimeSeriesConfig, Granularity
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from .base import SignAIghtSchema, Document


class StepPoint(str, Enum):
    entry = "entry"
    out = "out"
    processing = "processing"
    error = "error"


class ServiceStepMeta(BaseModel):
    search_id: UUID
    person_id: UUID
    executor: Optional[str] = None
    search_step: Optional[str] = None
    message: Optional[str] = None
    docs_count: Optional[int] = None
    step_duration_microseconds: Optional[float] = None
    step_point: Optional[StepPoint] = None


class ServiceStepLog(SignAIghtSchema):
    ts: datetime = Field(default_factory=datetime.now)
    meta: ServiceStepMeta


class ServiceStepLogModel(ServiceStepLog, Document):

    class Settings:
        name = "service_step_log"
        use_revision = False
        timeseries = TimeSeriesConfig(
            time_field="ts",
            meta_field="meta",
            granularity=Granularity.minutes,
            expire_after_seconds=7884000  # 90 days
        )
