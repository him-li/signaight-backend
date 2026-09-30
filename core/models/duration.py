from typing import Optional

from .base import SignAIghtSchema


class Duration(SignAIghtSchema):
    years: Optional[int] = None
    months: Optional[int] = None
