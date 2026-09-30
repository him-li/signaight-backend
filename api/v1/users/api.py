from fastapi import APIRouter, Depends
from api.auth import UserInfo, auth

router = APIRouter()


@router.get("/me")
async def get_current_user(
    userinfo: UserInfo = Depends(auth.current_user())
):
    return userinfo
