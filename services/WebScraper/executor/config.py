from pydantic import AnyHttpUrl, WebsocketUrl
from pydantic_settings import BaseSettings
from typing import Optional


class ProxySettings(BaseSettings):
    OXYLABS_PROXY_URI: Optional[AnyHttpUrl] = None
    OXYLABS_SERP_PROXY_URI: Optional[AnyHttpUrl] = None


class RedisSettings(BaseSettings):
    REDIS_URI: Optional[str] = None


class Settings(ProxySettings, RedisSettings):
    XING_USERNAME: Optional[str] = None
    XING_PASSWORD: Optional[str] = None
    XING_USER_TIMEZONE: Optional[str] = 'Europe/London'

    PLAYWRIGHT_BROWSER_SERVER: Optional[WebsocketUrl] = None

settings = Settings()
