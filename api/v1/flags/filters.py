from typing import List, Optional
from uuid import UUID
from core.models.search_state import SearchStatus
from pydantic import Field

from core.models import FlagModel, PersonModel
from api.filter import Filter


class FlagFilter(Filter):
    search: Optional[str] = None

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = FlagModel
        search_field_name = "search"
        search_model_fields = [""]

class FlagPersonsFilter(Filter):
    project__id: Optional[UUID] = None
    project__project_platform: Optional[str] = None
    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = PersonModel

