import uuid
from fastapi import APIRouter, Depends, status as http_status
from fastapi_filter import FilterDepends

from api.auth import AccessTokenInfo, auth, user_directory
from api.pagination import Page, Params

from .filters import RecalculationFilter
from .dependencies import RecalculationCRUD, get_recalculation_crud
from .schemas import RecalculationEventRead

router = APIRouter()


@router.get(
    "",
    response_model=Page[RecalculationEventRead],
    status_code=http_status.HTTP_200_OK
)
async def get_recalculations(
    params: Params = Depends(),
    filter: RecalculationFilter = FilterDepends(RecalculationFilter),
    recalculations: RecalculationCRUD = Depends(get_recalculation_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await user_directory.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    return await recalculations.read_list(params, filter, user_id)


@router.get(
    "/{id}",
    response_model=RecalculationEventRead,
    status_code=http_status.HTTP_200_OK
)
async def get_recalculation(
    id: uuid.UUID,
    recalculations: RecalculationCRUD = Depends(get_recalculation_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    return await recalculations.read(id)
