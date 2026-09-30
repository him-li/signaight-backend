from typing import List, Optional

from core.models import AlertsModel
from api.filter import Filter


class AlertsFilter(Filter):
    search: Optional[str] = None

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = AlertsModel
        search_field_name = "search"
        search_model_fields = [""]
