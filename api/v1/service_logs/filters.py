from uuid import UUID
from typing import List, Optional
from pydantic import Field

from core.models import ServiceStepLogModel
from api.filter import Filter


class ServiceStepLogFilter(Filter):
    search: Optional[str] = None
    meta__search_id: Optional[UUID] = Field(default=None, alias='search_id')
    meta__person_id: Optional[UUID] = Field(default=None, alias='person_id')
    meta__executor: Optional[str] = Field(default=None, alias='executor')
    meta__search_step: Optional[str] = Field(default=None, alias='search_step')

    order_by: Optional[List[str]] = None

    class Constants(Filter.Constants):
        model = ServiceStepLogModel
        search_field_name = "search"
        search_model_fields = [""]
