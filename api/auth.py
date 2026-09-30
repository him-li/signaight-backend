import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from typing_extensions import TypedDict
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.config import settings
from core.models import AuthUserModel


class FiefAccessTokenInfo(TypedDict, total=False):
    id: str
    sub: str
    email: str
    permissions: list[str]
    access_token: str
    exp: int


class FiefUserInfo(TypedDict, total=False):
    sub: str
    id: str
    email: str
    given_name: str
    family_name: str
    is_active: bool
    email_verified: bool
    permissions: list[str]


scheme = OAuth2PasswordBearer("/api/v1/auth/token", auto_error=True)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return "pbkdf2_sha256$310000${}${}".format(
        base64.urlsafe_b64encode(salt).decode(),
        base64.urlsafe_b64encode(digest).decode(),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            base64.urlsafe_b64decode(salt),
            int(iterations),
        )
        return hmac.compare_digest(
            base64.urlsafe_b64encode(digest).decode(), expected
        )
    except (TypeError, ValueError):
        return False


def user_info(user: AuthUserModel) -> FiefUserInfo:
    return {
        "sub": str(user.id),
        "id": str(user.id),
        "email": str(user.email),
        "given_name": user.first_name,
        "family_name": user.last_name,
        "is_active": user.is_active,
        "email_verified": user.email_verified,
        "permissions": user.permissions,
    }


def create_access_token(user: AuthUserModel) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    payload = {
        **user_info(user),
        "permissions": user.permissions,
        "exp": expires,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(
        payload, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
    )


def decode_access_token(token: str) -> FiefAccessTokenInfo:
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.AUTH_SECRET_KEY,
            algorithms=[settings.AUTH_ALGORITHM],
        )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    subject = payload.get("sub") or payload.get("id")
    if not subject:
        raise HTTPException(status_code=401, detail="Invalid access token")
    payload["id"] = str(subject)
    payload["sub"] = str(subject)
    payload["access_token"] = token
    payload.setdefault("permissions", ["signaight:user"])
    return payload  # type: ignore[return-value]


async def authenticated_dependency(
    token: str = Depends(scheme),
) -> FiefAccessTokenInfo:
    return decode_access_token(token)


async def current_user_dependency(
    token_info: FiefAccessTokenInfo = Depends(authenticated_dependency),
) -> FiefUserInfo:
    user = await AuthUserModel.get(UUID(token_info["id"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user_info(user)


class LocalAuth:
    def authenticated(self):
        return authenticated_dependency

    def current_user(self):
        return current_user_dependency


class LocalUserInfoClient:
    async def userinfo(self, token: str) -> FiefUserInfo:
        token_info = decode_access_token(token)
        user = await AuthUserModel.get(UUID(token_info["id"]))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_info(user)


auth = LocalAuth()
fief = LocalUserInfoClient()  # Compatibility alias while callers are migrated.


async def get_socket_user_id(access_token: str) -> str | None:
    try:
        return decode_access_token(access_token).get("id")
    except HTTPException:
        return None


def get_http_user_id(access_token_info: FiefAccessTokenInfo) -> str | None:
    return access_token_info.get("id")


__all__ = [
    "FiefAccessTokenInfo", "FiefUserInfo", "auth", "fief",
    "create_access_token", "hash_password", "verify_password", "user_info",
    "get_socket_user_id", "get_http_user_id",
]
