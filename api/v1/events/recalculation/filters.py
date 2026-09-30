from typing import List, Optional

from core.models import RecalculationEventModel
from api.filter import Filter


class RecalculationFilter(Filter):
    created_at: Optional[str] = None
    status: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = RecalculationEventModel
        search_field_name = "search"
        search_model_fields = [
            "status",
        ]
