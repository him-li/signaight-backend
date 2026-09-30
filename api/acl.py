"""Application-local authorization principal."""

from fastapi import Depends

from api.auth import FiefAccessTokenInfo, auth, fief
from api.local_authorization import Principal


async def get_principal(
    access_token_info: FiefAccessTokenInfo = Depends(auth.authenticated()),
) -> Principal:
    userinfo = await fief.userinfo(access_token_info["access_token"])
    return Principal(
        id=str(userinfo["sub"]),
        roles=frozenset(access_token_info.get("permissions", [])),
        is_active=bool(userinfo.get("is_active")),
        email_verified=bool(userinfo.get("email_verified")),
        email=userinfo.get("email"),
        first_name=userinfo.get("given_name") or "",
        last_name=userinfo.get("family_name") or "",
    )
