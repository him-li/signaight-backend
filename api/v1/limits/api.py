import uuid

import pendulum
from fastapi import APIRouter, Depends, status as http_status
from fastapi_filter import FilterDepends

from api.acl import Principal, get_principal
from core.models.resource_action_log import ResourceActionLogModel

from .filters import LimitsFilter
from .schemas import LimitsView

router = APIRouter()
PERSON_DAILY_LIMIT = 10


@router.get("", response_model=LimitsView, status_code=http_status.HTTP_200_OK,
            response_model_exclude_none=True, deprecated=True)
async def get_limits(
    filter: LimitsFilter = FilterDepends(LimitsFilter),
    principal: Principal = Depends(get_principal),
) -> LimitsView:
    current = await ResourceActionLogModel.find(
        ResourceActionLogModel.meta.user_id == uuid.UUID(principal.id),
        ResourceActionLogModel.meta.kind == filter.kind,
        ResourceActionLogModel.meta.action == "create",
        ResourceActionLogModel.ts >= pendulum.now().start_of("day"),
        ResourceActionLogModel.ts <= pendulum.now().end_of("day"),
    ).count()
    unlimited = principal.is_admin or filter.action != "create"
    limit = 0 if unlimited else PERSON_DAILY_LIMIT
    return LimitsView(limits=limit, current=current, kind=filter.kind,
                      allow=unlimited or current < PERSON_DAILY_LIMIT)
