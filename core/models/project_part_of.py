import datetime
from pydantic import Field
from typing import Optional, List, Any

from .base import SignAIghtSchema
from .member import Member


class ProjectPartOf(SignAIghtSchema):
    title: str = Field(..., examples=["title"])
    start_month_year: Optional[datetime.date] = Field(None, examples=["2019-01"])
    end_month_year: Optional[datetime.date] = Field(None, examples=["2020-01"])
    description: Optional[str] = Field(None, examples=["description"])
    contributors: Optional[Any] = None
    project_id: Optional[str] = Field(None, examples=["123456789"])
    members: Optional[List[Member]] = None
    occupation: Optional[str] = Field(None, examples=["occupation"])
    single_date: Optional[bool] = Field(None, examples=[True])
    url: Optional[str] = Field(None, examples=["url"])
