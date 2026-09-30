import uuid
from fastapi import (APIRouter, Depends,
                     status as http_status)
from fastapi_filter import FilterDepends

from api.auth import FiefAccessTokenInfo, auth
from api.pagination import Page, Params
from .filters import EvaluationFilter
from .dependencies import EvaluationCRUD, get_evaluation_crud
from .schemas import EvaluationRead, EvaluationCreate, EvaluationUpdate

router = APIRouter()


@router.get(
        "",
        response_model=Page[EvaluationRead],
        status_code=http_status.HTTP_200_OK
)
async def get_evaluations(
    params: Params = Depends(),
    filter: EvaluationFilter = FilterDepends(EvaluationFilter),
    evaluations: EvaluationCRUD = Depends(get_evaluation_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[EvaluationRead]:
    evaluation = await evaluations.read_list(params, filter)
    return evaluation


@router.get(
    "/by-person/{id}",
    response_model=Page[EvaluationRead],
    status_code=http_status.HTTP_200_OK
)
async def get_evaluation_by_person(
    id: uuid.UUID | str,
    params: Params = Depends(),
    filter: EvaluationFilter = FilterDepends(EvaluationFilter),
    evaluations: EvaluationCRUD = Depends(get_evaluation_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Page[EvaluationRead]:
    return await evaluations.read_all(params, filter, id)


@router.get(
        "/{id}",
        response_model=EvaluationRead,
        status_code=http_status.HTTP_200_OK
)
async def get_evaluation(
    id: uuid.UUID,
    evaluations: EvaluationCRUD = Depends(get_evaluation_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> EvaluationRead:
    return await evaluations.read(id)


@router.post(
    "",
    response_model=EvaluationRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_evaluation(
    evaluation: EvaluationCreate,
    evaluations: EvaluationCRUD = Depends(get_evaluation_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> EvaluationRead:
    return await evaluations.create(evaluation.model_dump())


@router.put(
    "/{evaluation_id}",
    response_model=EvaluationRead,
    response_description="Review record updated",
)
async def update_evaluation(
    evaluation_id: uuid.UUID,
    evaluation: EvaluationUpdate,
    evaluations: EvaluationCRUD = Depends(get_evaluation_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> EvaluationRead:
    return await evaluations.update(evaluation_id, evaluation.model_dump())
