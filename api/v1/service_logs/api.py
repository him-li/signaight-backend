import uuid
from fastapi import (APIRouter, Depends,
                     status as http_status,
                     Request, HTTPException)
from fastapi_filter import FilterDepends

from core.config import settings
from api.pagination import Page, Params
from .filters import ServiceStepLogFilter
from .dependencies import ServiceStepLogCRUD, get_service_step_logs_crud
from .schemas import ServiceStepLogRead, ServiceStepLogCreate

router = APIRouter()


@router.get(
    "",
    response_model=Page[ServiceStepLogRead],
    status_code=http_status.HTTP_200_OK
)
async def get_logs(
    request: Request,
    params: Params = Depends(),
    filter: ServiceStepLogFilter = FilterDepends(ServiceStepLogFilter),
    logs: ServiceStepLogCRUD = Depends(get_service_step_logs_crud),
) -> Page[ServiceStepLogRead]:
    x_api_key = request.headers.get("x-api-key")
    if not x_api_key or not x_api_key == settings.SERVICE_LOGS_API_KEY:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
    logs = await logs.list(params, filter)
    return logs


@router.get(
    "/{id}",
    response_model=ServiceStepLogRead,
    status_code=http_status.HTTP_200_OK
)
async def get_log(
    request: Request,
    id: uuid.UUID,
    logs: ServiceStepLogCRUD = Depends(get_service_step_logs_crud),
) -> ServiceStepLogRead:
    x_api_key = request.headers.get("x-api-key")
    if not x_api_key or not x_api_key == settings.SERVICE_LOGS_API_KEY:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
    return await logs.read(id)


@router.post(
    "",
    response_model=ServiceStepLogRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_log(
    request: Request,
    log: ServiceStepLogCreate,
    logs: ServiceStepLogCRUD = Depends(get_service_step_logs_crud),
) -> ServiceStepLogRead:
    x_api_key = request.headers.get("x-api-key")
    if not x_api_key or not x_api_key == settings.SERVICE_LOGS_API_KEY:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
    return await logs.create(log.model_dump())
