from typing import List, Optional

from core.models import SearchEventModel
from api.filter import Filter


class SearchFilter(Filter):
    context: Optional[str] = None
    created_at: Optional[str] = None
    status: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = SearchEventModel
        search_field_name = "search"
        search_model_fields = [
            "status",
        ]
