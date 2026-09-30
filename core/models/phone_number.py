from pydantic import Field
from typing import Optional
from enum import Enum

from .base import SignAIghtSchema


class PhoneType(Enum):
    Mobile = "Mobile"
    Home = "Home"
    Work = "Work"
    Other = "Other"


class PhoneNumber(SignAIghtSchema):
    number: str = Field(..., examples=["123456789"])
    type: Optional[PhoneType] = Field(None, examples=["Mobile"])
