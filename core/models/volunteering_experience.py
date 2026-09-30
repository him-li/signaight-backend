import datetime
from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema
from .duration import Duration


class VolunteeringExperience(SignAIghtSchema):
    role: str = Field(..., examples=["role"])
    company_name: str = Field(..., examples=["company_name"])
    is_current: Optional[bool] = None
    start_month_year: Optional[datetime.date] = None
    end_month_year: Optional[datetime.date] = None
    duration: Optional[Duration] = None
    description: Optional[str] = Field(None, examples=["description"])
