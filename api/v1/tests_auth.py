from fastapi import APIRouter, Depends
from api.auth import FiefAccessTokenInfo, auth
from typing import Optional


router = APIRouter()


@router.get("/authenticated")
async def get_authenticated(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated())
):
    return access_token_info


@router.get("/authenticated-optional")
async def get_authenticated_optional(
    access_token_info: Optional[FiefAccessTokenInfo] = Depends(
        auth.authenticated(optional=True)
    ),
):
    return access_token_info


@router.get("/authenticated-scope")
async def get_authenticated_scope(
    access_token_info: FiefAccessTokenInfo = Depends(
        auth.authenticated(scope=["offline_access"])
    ),
):
    return access_token_info
