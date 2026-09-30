import uuid
from fastapi import APIRouter, Depends, status as http_status
from fastapi_filter import FilterDepends

from api.auth import AccessTokenInfo, auth, user_directory
from api.pagination import Page, Params
from api.socketio import socket_manager

from core.socketio import MessageBuilder

from .filters import SearchFilter
from .dependencies import SearchCRUD, get_search_crud
from .schemas import SearchEventRead

router = APIRouter()


@router.get(
        "",
        response_model=Page[SearchEventRead],
        status_code=http_status.HTTP_200_OK
        )
async def get_searches(
    params: Params = Depends(),
    filter: SearchFilter = FilterDepends(SearchFilter),
    searches: SearchCRUD = Depends(get_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await user_directory.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    return await searches.read_list(params, filter, user_id)


@router.get(
        "/{id}",
        response_model=SearchEventRead,
        status_code=http_status.HTTP_200_OK
        )
async def get_search(
    id: uuid.UUID,
    searches: SearchCRUD = Depends(get_search_crud),
    access_token_info: AccessTokenInfo = Depends(auth.authenticated()),
):
    user_info = await user_directory.userinfo(access_token_info.get("access_token"))
    user_id = user_info.get("sub")
    await searches.update(id, {"status": "Seen"})
    message = MessageBuilder.search_message(id, "seen")
    await socket_manager.send_message_by_user_id(user_id, message)
    return await searches.read(id)
