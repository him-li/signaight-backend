import datetime
from typing import Optional, Union
from pydantic import AnyHttpUrl

from .base import SignAIghtSchema


class Recommender(SignAIghtSchema):
    linkedin_full_name: str
    linkedin_headline: Optional[str] = None


class Recommendation(SignAIghtSchema):
    recommender: Recommender
    date: Optional[Union[str, datetime.date]] = None
    context: Optional[str] = None
    description: Optional[str] = None
    url: Optional[AnyHttpUrl] = None
