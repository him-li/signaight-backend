from pydantic import field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List, Union, Optional
from core.config import Settings as CoreSettings


class AuthSettings(BaseSettings):
    AUTH_SECRET_KEY: str = "change-me-before-production"
    AUTH_ALGORITHM: str = "HS256"


class Settings(AuthSettings, CoreSettings):
    PROJECT_NAME: str = "SignAIght Cloud API"
    API_PREFIX: str = "api"
    API_VERSION: str = "v1"

    SERVER_HOST: Optional[AnyHttpUrl] = None
    # SERVER_AUTH_BASE: AnyHttpUrl

    # 60 seconds * 60 minutes * 1 hours = 1 hour
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 10
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200",
    # "http://localhost:3000", "http://localhost:8080",
    # "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
        cls,
        v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        elif not v:
            return ['*']
        raise ValueError(v)

    ALLOW_USERS_REGISTER: bool = True


settings = Settings()
