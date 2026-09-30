from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field


MergeMode = Literal["auto", "manual"]
ConflictResolution = Literal["last_updated", "manual"]
ArrayMergeStrategy = Literal["union", "last_updated", "replace"]


class MergeStrategy(BaseModel):
    conflict_resolution: ConflictResolution = "last_updated"
    merged_arrays: Optional[ArrayMergeStrategy] = "union"


class MergedBy(BaseModel):
    user_id: str
    email: Optional[str] = None


class MergeMetadata(BaseModel):
    merged_from_person_ids: List[str] = Field(
        ..., description="IDs of persons merged into this one"
    )
    merge_mode: MergeMode
    merged_at: datetime = Field(default_factory=datetime.utcnow)
    merged_by: Optional[MergedBy] = None
    merge_strategy: Optional[MergeStrategy] = None
