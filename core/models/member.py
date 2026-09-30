from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema


class Member(SignAIghtSchema):
    member_id: Optional[str] = Field(None, examples=["123456789"])
    name: Optional[str] = Field(None, examples=["name"])
