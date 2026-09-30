from typing import Optional, Union
from datetime import date

from .base import SignAIghtSchema


class Period(SignAIghtSchema):
    date_from: Optional[Union[str, date, None]] = None
    date_to: Optional[Union[str, date, None]] = None
