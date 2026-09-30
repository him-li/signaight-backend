from typing import Annotated

from beanie.exceptions import RevisionIdWasChanged
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from pymongo.errors import DuplicateKeyError

from api.auth import (
    UserInfo,
    auth,
    create_access_token,
    hash_password,
    user_info,
    verify_password,
)
from api.config import settings
from core.models import AuthUserModel

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(default="", max_length=100)
    last_name: str = Field(default="", max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest) -> TokenResponse:
    if not settings.ALLOW_USERS_REGISTER:
        raise HTTPException(status_code=403, detail="Registration is disabled")
    email = payload.email.lower()
    if await AuthUserModel.find_one(AuthUserModel.email == email):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = AuthUserModel(
        email=email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
    )
    try:
        await user.insert()
    except (DuplicateKeyError, RevisionIdWasChanged) as exc:
        raise HTTPException(status_code=409, detail="Email is already registered") from exc
    token = create_access_token(user)
    return TokenResponse(access_token=token, user=user_info(user))


@router.post("/token", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    email = form.username.lower()
    user = await AuthUserModel.find_one(AuthUserModel.email == email)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    token = create_access_token(user)
    return TokenResponse(access_token=token, user=user_info(user))


@router.get("/me", response_model=UserInfo)
async def me(user: UserInfo = Depends(auth.current_user())) -> UserInfo:
    return user
