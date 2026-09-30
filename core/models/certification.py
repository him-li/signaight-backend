from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema


class Certification(SignAIghtSchema):
    certification_id: Optional[str] = Field(None, examples=["123456789"])
    authority: Optional[str] = Field(None, examples=["authority"])
    company: Optional[str] = Field(None, examples=["company"])
    end_month_year: Optional[str] = Field(None, examples=["2020-01"])
    license_number: Optional[str] = Field(None, examples=["license_number"])
    name: Optional[str] = Field(None, examples=["name"])
    start_month_year: Optional[str] = Field(None, examples=["2019-01"])
    url: Optional[str] = Field(None, examples=["url"])
