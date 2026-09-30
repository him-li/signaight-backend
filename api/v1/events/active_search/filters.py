from typing import List, Optional

from core.models import ActiveSearchEventModel
from api.filter import Filter


class ActiveSearchFilter(Filter):
    created_at: Optional[str] = None
    status: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = ActiveSearchEventModel
        search_field_name = "search"
        search_model_fields = [
            "status",
        ]
