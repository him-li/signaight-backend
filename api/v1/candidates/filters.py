from typing import List, Optional

from core.models import CandidateModel
from api.filter import Filter


class CandidateFilter(Filter):
    search: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    education: Optional[str] = None
    signaight_score: Optional[int] = None
    signaight_score__gte: Optional[int] = None
    signaight_score__lte: Optional[int] = None

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = CandidateModel
        search_field_name = "search"
        search_model_fields = ["name", "title", "education"]
