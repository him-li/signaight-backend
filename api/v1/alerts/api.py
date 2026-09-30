import uuid
from fastapi import (APIRouter, Depends,
                     status as http_status)
from fastapi_filter import FilterDepends

from api.auth import AccessTokenInfo, auth
from api.pagination import Page, Params
from .filters import AlertsFilter
from .dependencies import AlertsCRUD, get_alerts_crud
from .schemas import AlertsRead, AlertsCreate, AlertsUpdate

router = APIRouter()


@router.get(
        "",
        response_model=Page[AlertsRead],
        status_code=http_status.HTTP_200_OK
)
async def get_alerts(
    params: Params = Depends(),
    filter: AlertsFilter = FilterDepends(AlertsFilter),
    alerts: AlertsCRUD = Depends(get_alerts_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> Page[AlertsRead]:
    alerts = await alerts.read_list(params, filter)
    return alerts


@router.get(
    "/by-person/{id}",
    response_model=Page[AlertsRead],
    status_code=http_status.HTTP_200_OK
)
async def get_alerts_by_person(
    id: uuid.UUID | str,
    params: Params = Depends(),
    filter: AlertsFilter = FilterDepends(AlertsFilter),
    alerts: AlertsCRUD = Depends(get_alerts_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> Page[AlertsRead]:
    return await alerts.read_all(params, filter, id)


@router.get(
        "/{id}",
        response_model=AlertsRead,
        status_code=http_status.HTTP_200_OK
)
async def get_alert(
    id: uuid.UUID,
    alerts: AlertsCRUD = Depends(get_alerts_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> AlertsRead:
    return await alerts.read(id)


@router.post(
    "",
    response_model=AlertsRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_alert(
    alert: AlertsCreate,
    alerts: AlertsCRUD = Depends(get_alerts_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> AlertsRead:
    return await alerts.create(alert.model_dump())


@router.put(
    "/{alert_id}",
    response_model=AlertsRead,
    response_description="Review record updated",
)
async def update_alert(
    alert_id: uuid.UUID,
    alert: AlertsUpdate,
    alerts: AlertsCRUD = Depends(get_alerts_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> AlertsRead:
    return await alerts.update(alert_id, alert.model_dump())
