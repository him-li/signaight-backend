import datetime
from pydantic import Field
from typing import Optional
#from datetime import date as datetype

from .base import SignAIghtSchema


class TestScore(SignAIghtSchema):
    date: Optional[datetime.date] = None
    description: Optional[str] = Field(None, examples=["description"])
    test_name: str = Field(..., examples=["name"])
    occupation: Optional[str] = Field(None, examples=["Software Engineer"])
    score: Optional[str] = Field(None, examples=["100"])
