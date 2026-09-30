from typing import List, Optional

from core.models import EvaluationModel
from api.filter import Filter


class EvaluationFilter(Filter):
    search: Optional[str] = None

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = EvaluationModel
        search_field_name = "search"
        search_model_fields = [""]
