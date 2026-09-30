from pydantic import Field

from core.config import StorageSettings, DatabaseSettings
from pydantic_settings import BaseSettings


class ExecutorSettings(StorageSettings, DatabaseSettings, BaseSettings):
    FACE_COMPARE_BASE_URL: str = Field("http://172.31.36.28:5020")
    FACE_COMPARE_API_KEY: str = Field("11sae")


settings = ExecutorSettings()
