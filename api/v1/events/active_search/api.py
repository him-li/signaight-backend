import asyncio
import uuid
from fastapi import APIRouter, Depends, status as http_status, BackgroundTasks
from fastapi_filter import FilterDepends

from api.auth import AccessTokenInfo, auth, user_directory, UserInfo
from api.pagination import Page, Params
from api.socketio import socket_manager

from core.config import settings
from core.socketio import MessageBuilder
from core.utils import transform_user_info

from tasks.app import run_active_search

from .filters import ActiveSearchFilter
from .dependencies import ActiveSearchCRUD, get_active_search_crud
from .schemas import (ActiveSearchEventRead,
                      ActiveSearchEventCreate, ActiveSearchEventUpdate)

router = APIRouter()


@router.get(
    "",
    response_model=Page[ActiveSearchEventRead],
    status_code=http_status.HTTP_200_OK
)
async def get_active_searches(
    params: Params = Depends(),
    filter: ActiveSearchFilter = FilterDepends(ActiveSearchFilter),
    active_searches: ActiveSearchCRUD = Depends(get_active_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await user_directory.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    return await active_searches.read_list(params, filter, user_id)


@router.get(
    "/{id}",
    response_model=ActiveSearchEventRead,
    status_code=http_status.HTTP_200_OK
)
async def get_active_search(
    id: uuid.UUID,
    active_searches: ActiveSearchCRUD = Depends(get_active_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    return await active_searches.read(id)


@router.post(
    "",
    response_model=ActiveSearchEventRead,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_active_search(
    active_search: ActiveSearchEventCreate,
    background_tasks: BackgroundTasks,
    active_searches: ActiveSearchCRUD = Depends(get_active_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
    user_info: UserInfo = Depends(auth.current_user()),
) -> ActiveSearchEventRead:
    user_info = transform_user_info(user_info)
    user_id = user_info.get("id")
    active_search.user_id = user_id
    active_search = await active_searches.create(active_search.model_dump())
    background_tasks.add_task(
        asyncio.get_event_loop().create_task,
        make_active_search(
            active_search
        ),
    )
    message = MessageBuilder.active_search_message(active_search.id, "added")
    await socket_manager.send_message_by_user_id(user_id, message)
    return active_search


@router.put(
    "/{active_search_id}",
    response_model=ActiveSearchEventRead,
    response_description="Review record updated",
)
async def update_active_search(
    active_search_id: uuid.UUID,
    active_search: ActiveSearchEventUpdate,
    active_searches: ActiveSearchCRUD = Depends(get_active_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
) -> ActiveSearchEventRead:
    return await active_searches.update(active_search_id,
                                        active_search.model_dump())


async def make_active_search(active_search):
    if settings.JINA_REMOTE_FLOW_LINKEDIN:
        await run_active_search.kiq(
            str(active_search.id))
    else:
        await run_active_search(active_search.id)

    return active_search
