import uuid
from fastapi import APIRouter, Response, Depends, status as http_status
from fastapi_filter import FilterDepends

from api.auth import AccessTokenInfo, auth
from api.pagination import Page, Params

from .filters import CandidateFilter
from .dependencies import CandidatesCRUD, get_candidates_crud
from .schemas import CandidateRead, CandidateCreate, CandidateUpdate


router = APIRouter()


@router.get(
    "/",
    response_model=Page[CandidateRead],
    status_code=http_status.HTTP_200_OK
)
async def get_candidates(
    params: Params = Depends(),
    filter: CandidateFilter = FilterDepends(CandidateFilter),
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> Page[CandidateRead]:
    return await candidates.read_list(params, filter)


@router.get(
    "/{id}",
    response_model=CandidateRead,
    status_code=http_status.HTTP_200_OK
)
async def get_candidate(
    id: uuid.UUID,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    return await candidates.read(id)


@router.post(
    "/",
    response_model=CandidateRead,
    status_code=http_status.HTTP_201_CREATED
)
async def add_candidate(
    candidate: CandidateCreate,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    return await candidates.create(candidate.model_dump())


@router.put(
    "/{id}",
    response_model=CandidateRead,
    response_description="Review record updated"
)
async def update_candidate(
    id: uuid.UUID,
    candidate: CandidateUpdate,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> CandidateRead:
    return await candidates.update(id, candidate.model_dump())


@router.delete(
    "/{id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_candidate(
    id: uuid.UUID,
    candidates: CandidatesCRUD = Depends(get_candidates_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    await candidates.delete(id)
