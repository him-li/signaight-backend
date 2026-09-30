import os
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# workaround for non dockerised app run
# WARNING: Place of this string is important
env_path = f"{os.path.dirname(os.path.realpath(__file__))}/../.env"
if os.path.isfile(env_path):
    load_dotenv(env_path)

from core.config import Settings as CoreSettings


class LangsearchSettings(BaseSettings):
    GOOGLE_GEMINI_API_KEY: str = Field(..., alias="GEMINI_API_KEY")
    GOOGLE_GEMINI_MODEL_NAME: str = Field("gemini-3-pro-preview",
        alias="GOOGLE_MODEL_NAME")
    GOOGLE_MODEL_PROVIDER: str = Field("google_genai", alias="MODEL_PROVIDER")
    OXYLABS_SERP_PROXY_USERNAME: str = Field(..., alias="OXYLABS_USERNAME")
    OXYLABS_SERP_PROXY_PASSWORD: str = Field(..., alias="OXYLABS_PASSWORD")
    OXYLABS_PROXY_UNBLOCKER_URL: AnyHttpUrl = Field(...,
        alias="PROXY_UNBLOCKER_URL")
    SEARCH_OUT_FILE_PATH: str = "./google_results.csv"

    model_config = SettingsConfigDict(
        validate_by_name=True,
        extra='ignore'
    )


from enum import Enum
from pydantic import RedisDsn, AmqpDsn, PostgresDsn, NatsDsn, model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from typing_extensions import Self

from core.config import (Settings as CoreSettings, RedisSettings,
    RabbitMQSettings)


class RedisBrokerSettings(RedisSettings):
    pass


class AioPikaBrokerSettings(RabbitMQSettings):
    RABBITMQ_URI: Optional[AmqpDsn] = None
    TASKIQ_AIOPIKABROKER_QOS: int = 10
    TASKIQ_AIOPIKABROKER_DECLARE_EXCHANGE: bool = True
    TASKIQ_AIOPIKABROKER_MAX_PRIORITY: int = 5
    TASKIQ_AIOPIKABROKER_QUEUE_DURABLE: bool = True


class PostgresBrokerSettings(BaseSettings):
    POSTGRES_URI: Optional[PostgresDsn] = None


class NatsBrokerSettings(BaseSettings):
    NATS_URI: Optional[NatsDsn] = None


class BrokersEnum(str, Enum):
    redis = 'redis'
    amqp = 'amqp'
    postgres = 'postgres'
    nats = 'nats'


class Settings(
    LangsearchSettings,
    NatsBrokerSettings,
    PostgresBrokerSettings,
    AioPikaBrokerSettings,
    RedisBrokerSettings,
    CoreSettings
):
    TASKIQ_TASK_DEFAULT_TIMEOUT: int = 3600
    TASKIQ_TASK_RETRY_ON_ERRORS: bool = True
    TASKIQ_TASK_MAX_RETRIES: int = 1
    # NOTE: this value in seconds Default: 91 days in seconds
    TASKIQ_GARBAGE_COLLECTOR_DELTA: int = 91*24*60*60
    # NOTE: this value in seconds Default: 2 hours in seconds
    TASKIQ_BROKEN_SEARCHED_ITEMS_DELTA: int = 2*60*60
    TASKIQ_QUEUE_NAME: str = 'signaight-ls'
    TASKIQ_BROKER: BrokersEnum = BrokersEnum.amqp

    @model_validator(mode='after')
    def check_backend_requirements(self) -> Self:
        match self.TASKIQ_BROKER:
            case BrokersEnum.amqp:
                if not self.RABBITMQ_URI:
                    raise ValueError('RABBITMQ_URI environment variable should'
                        ' configured in .env or passed to container')
            case BrokersEnum.postgres:
                if not self.POSTGRES_URI:
                    raise ValueError('POSTGRES_URI environment variable should'
                        ' configured in .env or passed to container')
            case BrokersEnum.nats:
                if not self.NATS_URI:
                    raise ValueError('NATS_URI environment variable should'
                        ' configured in .env or passed to container')
        return self

    MLFLOW_TRACKING_URI: Optional[str] = None

    model_config = SettingsConfigDict(
        extra='ignore',
        validate_by_name=True,
        case_sensitive=True,
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = Settings()
