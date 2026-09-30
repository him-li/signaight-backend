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
    TASKIQ_AIOPIKABROKER_QUEUE_DURABLE:  bool = True


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

    TASKIQ_QUEUE_NAME: str = 'signaight'
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


settings = Settings()
