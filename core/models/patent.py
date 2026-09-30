import datetime
from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema
from .member import Member


class Patent(SignAIghtSchema):
    patent_id: Optional[str] = Field(None, examples=["123456789"])
    application_number: Optional[str] = Field(None, examples=["application_number"])
    description: Optional[str] = Field(None, examples=["description"])
    filling_date: Optional[datetime.date] = Field(None, examples=["2020-01-01"])
    inventors: Optional[List[Member]] = None
    issue_date: Optional[datetime.date] = Field(None, examples=["2020-01-01"])
    issuer: str = Field(..., examples=["issuer"])
    number: Optional[str] = Field(None, examples=["number"])
    pending: bool = Field(..., examples=[True])
    title: str = Field(..., examples=["title"])
    url: Optional[str] = Field(None, examples=["url"])
