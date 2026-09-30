from fastapi import APIRouter, Depends
from api.auth import FiefUserInfo, auth

router = APIRouter()


@router.get("/me")
async def get_current_user(
    userinfo: FiefUserInfo = Depends(auth.current_user())
):
    return userinfo
