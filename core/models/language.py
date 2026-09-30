from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema


class Language(SignAIghtSchema):
    language_id: Optional[str] = Field(None, examples=["123456789"])
    language: str = Field(..., examples=["English"])
    proficiency: Optional[str] = Field(None, examples=["Fluent"])
