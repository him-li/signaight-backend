import uuid
from fastapi import (
    APIRouter, Response,
    Depends, status as http_status)
from fastapi_filter import FilterDepends

from api.auth import FiefAccessTokenInfo, auth
from api.pagination import Page, Params

from .filters import MappingFilter
from .dependencies import MappingsCRUD, get_mappings_crud
from .schemas import MappingRead, MappingCreate, MappingUpdate

router = APIRouter()


@router.get(
        "/",
        response_model=Page[MappingRead],
        status_code=http_status.HTTP_200_OK
)
async def get_mappings(
    params: Params = Depends(),
    filter: MappingFilter = FilterDepends(MappingFilter),
    mappings: MappingsCRUD = Depends(get_mappings_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[MappingRead]:
    return await mappings.read_list(params, filter)


@router.get("/{id}", response_model=MappingRead,
            status_code=http_status.HTTP_200_OK)
async def get_mapping(
    id: uuid.UUID,
    mappings: MappingsCRUD = Depends(get_mappings_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> MappingRead:
    return await mappings.read(id)


@router.post(
        "/",
        response_model=MappingRead,
        status_code=http_status.HTTP_201_CREATED
)
async def add_mapping(
    mapping: MappingCreate,
    mappings: MappingsCRUD = Depends(get_mappings_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> MappingRead:
    return await mappings.create(mapping.model_dump())


@router.put(
    "/{id}",
    response_model=MappingRead,
    response_description="Review record updated"
)
async def update_mapping(
    id: uuid.UUID,
    mapping: MappingUpdate,
    mappings: MappingsCRUD = Depends(get_mappings_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> MappingRead:
    return await mappings.update(id, mapping.model_dump())


@router.delete(
    "/{id}",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT
)
async def delete_mapping(
    id: uuid.UUID,
    mappings: MappingsCRUD = Depends(get_mappings_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    await mappings.delete(id)
