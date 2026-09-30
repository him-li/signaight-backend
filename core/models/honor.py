import datetime
from pydantic import Field
from typing import Optional
from datetime import date


from .base import SignAIghtSchema


class Honor(SignAIghtSchema):
    honor_id: Optional[str] = Field(None, examples=["123456789"])
    description: Optional[str] = Field(None, examples=["description"])
    issue_date: Optional[datetime.date] = Field(None, examples=["2020-01"])
    issuer: Optional[str] = Field(None, examples=["issuer"])
    occupation: Optional[str] = Field(None, examples=["occupation"])
    title: str = Field(..., examples=["title"])
    associated_with: Optional[str] = Field(
        None, examples=["Associated with University of California, Davis"])
