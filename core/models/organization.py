from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema


class Organization(SignAIghtSchema):
    organization_id: Optional[str] = Field(None, examples=["123456789"])
    description: Optional[str] = Field(None, examples=["description"])
    end_month_year: Optional[str] = Field(None, examples=["2020-01"])
    name: Optional[str] = Field(None, examples=["Google"])
    occupation: Optional[str] = Field(None, examples=["Software Engineer"])
    position: Optional[str] = Field(None, examples=["Software Engineer"])
    start_month_year: Optional[str] = Field(None, examples=["2019-01"])
