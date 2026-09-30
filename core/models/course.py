from pydantic import Field
from typing import Optional

from .base import SignAIghtSchema


class Course(SignAIghtSchema):
    course_code: Optional[str] = Field(None, examples=["123456789"])
    course_name: Optional[str] = Field(None, examples=["name"])
