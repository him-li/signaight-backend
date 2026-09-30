from typing import List, Optional

from core.models import MappingModel
from api.filter import Filter


class MappingFilter(Filter):
    search: Optional[str]
    source: Optional[str]
    resource: Optional[str]

    order_by: Optional[List[str]]

    class Constants(Filter.Constants):
        model = MappingModel
        search_field_name = "search"
        search_model_fields = ["source", "resource"]
