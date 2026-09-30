import datetime
from pydantic import Field
from typing import Optional, List

from .base import SignAIghtSchema
from .member import Member


class Publication(SignAIghtSchema):
    publication_id: Optional[str] = Field(None, examples=["123456789"])
    authors: Optional[List[Member]] = None
    publication_date: Optional[datetime.date] = Field(None, examples=["2020-01-01"])
    description: Optional[str] = Field(None, examples=["description"])
    name: str = Field(..., examples=["name"])
    publisher: Optional[str] = Field(None, examples=["publisher"])
    url: Optional[str] = Field(None, examples=["url"])
