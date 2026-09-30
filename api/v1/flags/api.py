import uuid
from fastapi import (APIRouter, Depends,
                     status as http_status)
from fastapi_filter import FilterDepends

from api.auth import FiefAccessTokenInfo, auth
from api.pagination import Page, Params
from .filters import FlagFilter, FlagPersonsFilter
from .dependencies import FlagsCRUD, get_flags_crud
from .schemas import FlagRead, FlagCreate, FlagUpdate, RedFlagStats

router = APIRouter()


@router.get(
    "",
    response_model=Page[FlagRead],
    status_code=http_status.HTTP_200_OK
)
async def get_flags(
    params: Params = Depends(),
    filter: FlagFilter = FilterDepends(FlagFilter),
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[FlagRead]:
    flags = await flags.list(params, filter)
    return flags


@router.get(
    "/by-person/{id}",
    response_model=Page[FlagRead],
    status_code=http_status.HTTP_200_OK
)
async def get_flags_by_person(
    id: uuid.UUID | str,
    params: Params = Depends(),
    filter: FlagFilter = FilterDepends(FlagFilter),
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[FlagRead]:
    return await flags.read_all_flags_by_person(params, filter, id)


@router.get(
    "/statistic",
    response_model=RedFlagStats,
    status_code=http_status.HTTP_200_OK
)
async def get_flags_statisctic(
    params: Params = Depends(),
    filter: FlagPersonsFilter = FilterDepends(FlagPersonsFilter),
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> RedFlagStats:
    return await flags.statistics(params, filter)


@router.get(
    "/{id}",
    response_model=FlagRead,
    status_code=http_status.HTTP_200_OK
)
async def get_flag(
    id: uuid.UUID,
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> FlagRead:
    return await flags.read(id)


@router.post(
    "",
    response_model=FlagRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_flag(
    flag: FlagCreate,
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> FlagRead:
    return await flags.create(flag.model_dump())


@router.put(
    "/{flag_id}",
    response_model=FlagRead,
    response_description="Review record updated",
)
async def update_flag(
    flag_id: uuid.UUID,
    flag: FlagUpdate,
    flags: FlagsCRUD = Depends(get_flags_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> FlagRead:
    return await flags.update(flag_id, flag.model_dump())
