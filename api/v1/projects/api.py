import pendulum
import uuid
from fastapi import (
    APIRouter,
    Response,
    Depends,
    status as http_status,
    BackgroundTasks,
)
from fastapi_filter import FilterDepends
from typing import Optional, List

from api.auth import FiefAccessTokenInfo, auth, fief, FiefUserInfo
from api.pagination import Page, Params
from api.socketio import socket_manager
from api.v1.flows.api import search_persons
from api.v1.persons.schemas import PersonRead
from api.v1.persons.dependencies import PersonsCRUD, get_persons_crud

from core.socketio import MessageBuilder
from core.utils import transform_user_info

from tasks.app import (recalculate_project_persons_score,
                       recalculate_project_persons_score_heuristics)

from .filters import ProjectFilter
from .dependencies import ProjectsCRUD, get_projects_crud
from .schemas import (ProjectRead, ProjectCreate,
                      ProjectUpdate, ProjectListRead, PersonRankingView)


router = APIRouter()


@router.get(
    "",
    response_model=Page[ProjectListRead],
    status_code=http_status.HTTP_200_OK
)
async def get_projects(
    params: Params = Depends(),
    filter: ProjectFilter = FilterDepends(ProjectFilter),
    projects: ProjectsCRUD = Depends(get_projects_crud),
) -> Page[ProjectListRead]:
    return await projects.list(params, filter)


@router.get(
    "/{id}",
    response_model=ProjectRead,
    status_code=http_status.HTTP_200_OK
)
async def get_project(
    id: uuid.UUID,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> ProjectRead:
    return await projects.read(id)


@router.get(
    "/{id}/leaderboard-info",
    status_code=http_status.HTTP_200_OK
)
async def get_leaderboard_info(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    projects_id = [id]
    if id == "all-projects":
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        projects_id = await projects.read_list_ids(user_id)
    else:
        await projects.read(id)
    return await projects.read_leaderboard_info_by_projects(projects_id)


@router.get(
    "/{id}/leaderboard-widgets",
    status_code=http_status.HTTP_200_OK
)
async def get_leaderboard_widgets(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    projects_id = [id]
    if id == "all-projects":
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        projects_id = await projects.read_list_ids(user_id)
    else:
        await projects.read(id)
    return await projects.read_leaderboard_widgets_by_projects(projects_id)

@router.get(
    "/{id}/riskmatrix-widgets",
    status_code=http_status.HTTP_200_OK
)
async def get_riskmatrix_widgets(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    projects_id = [id]
    if id == "all-projects":
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        projects_id = await projects.read_list_ids(user_id)
    else:
        await projects.read(id)
    return await projects.read_riskmatrix_widgets_by_projects(projects_id)


@router.get(
    "/{id}/basic-info",
    status_code=http_status.HTTP_200_OK,
    response_model=List[PersonRead],
    response_model_exclude_none=True,
)
async def get_person_basic_data(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    projects_id = [id]
    if id == "all-projects":
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        projects_id = await projects.read_list_ids(user_id)
    else:
        await projects.read(id)
    return await projects.read_basic_data_by_projects(projects_id)


@router.get(
    "/{id}/ranking",
    status_code=http_status.HTTP_200_OK,
    response_model=List[PersonRead],
    response_model_exclude_none=True,
)
async def get_person_ranking_data(
    id: uuid.UUID | str,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    projects_id = [id]
    if id == "all-projects":
        user_info = await fief.userinfo(access_token_info.get("access_token"))
        user_id = user_info.get("sub")
        projects_id = await projects.read_list_ids(user_id)
    else:
        await projects.read(id)
    return await projects.read_ranking_by_projects(projects_id)


@router.get(
    "/{id}/refresh-all",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT,
)
async def refresh_all_persons_search(
    id: uuid.UUID,
    background_tasks: BackgroundTasks,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    persons: PersonsCRUD = Depends(get_persons_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
    user_info: FiefUserInfo = Depends(auth.current_user()),
):
    await projects.read(id)
    user_info = transform_user_info(user_info)
    user_id = user_info.get("id")
    persons_ids_list = await persons.read_ids_list_by_project(id)
    for person_id in persons_ids_list:
        request_body = {"selected_persons": [person_id],
                        "flow_names": ["Search_All"]}
        await search_persons(
            request_body,
            background_tasks,
            persons,
            access_token_info,
        )
    message = MessageBuilder.project_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_id, message)


@router.post(
    "",
    response_model=ProjectRead,
    status_code=http_status.HTTP_201_CREATED
)
async def add_project(
    project: ProjectCreate,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> ProjectRead:
    user_info = await fief.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    user_email = user_info.get("email", None)
    project.user_email = user_email
    # TODO: Potential DRY violation. Should be moved into mode as field validator
    # if not project.person_ruleset:
    #    project.person_ruleset = person_ruleset
    project = await projects.create(project.model_dump(), user_id)
    message = MessageBuilder.project_message(project.id, "added")
    await socket_manager.send_message_by_user_id(user_id, message)
    return project


@router.put(
    "/{id}",
    response_model=ProjectRead,
    response_description="Review record updated"
)
async def update_project(
    id: uuid.UUID,
    project: ProjectUpdate,
    full_recalculation: Optional[bool] = False,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> ProjectRead:
    user_info = await fief.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    project.updated_at = pendulum.now()
    updated_project = await projects.update(id, project.model_dump())
    if full_recalculation:
        await recalculate_project_persons_score_heuristics.kiq(str(id))
    else:
        await recalculate_project_persons_score.kiq(str(id))
    message = MessageBuilder.project_message(id, "updated")
    await socket_manager.send_message_by_user_id(user_id, message)
    return updated_project


@router.delete(
    "/{id}",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT
)
async def delete_project(
    id: uuid.UUID,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await fief.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    await projects.delete(id)
    message = MessageBuilder.project_message(id, "deleted")
    await socket_manager.send_message_by_user_id(user_id, message)


@router.get(
    "/{id}/cleanup",
    response_class=Response,
    status_code=http_status.HTTP_204_NO_CONTENT
)
async def cleanup_project(
    id: uuid.UUID,
    projects: ProjectsCRUD = Depends(get_projects_crud),
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
):
    await projects.cleanup(id)
