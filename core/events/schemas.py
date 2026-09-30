from typing import Optional
from pydantic import Field
from datetime import timedelta

from core.models import SearchEventModel


class SearchEventCreate(SearchEventModel):
    # context describe for which flow search has been ran
    context: str = Field(..., examples=["DeepSearch"])
    duration: Optional[timedelta] = Field(examples=[1000])
    retries: Optional[int] = Field(default=0, examples=[10])
    percent_completed: Optional[int] = Field(default=0,
                                             gt=0,
                                             le=100,
                                             examples=[10])
