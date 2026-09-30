from typing import Optional
from pydantic import (
    AnyUrl,
    AnyHttpUrl,
    model_validator,
    field_validator
)
from pydantic_settings import BaseSettings
from typing_extensions import Self


from typing import Annotated

from pydantic.networks import UrlConstraints
from pydantic_core import MultiHostUrl

# NOTE: we use custom typ for mongo just to avoid dsnparse lib and due bug in
# pydantic https://github.com/pydantic/pydantic/issues/7331
MongoSrvDsn = Annotated[MultiHostUrl,
                        UrlConstraints(allowed_schemes=['mongodb', 'mongodb+srv'])]


class DatabaseSettings(BaseSettings):
    MONGODB_URI: MongoSrvDsn


class RedisSettings(BaseSettings):
    REDIS_URI: Optional[str] = None


class RabbitMQSettings(BaseSettings):
    RABBITMQ_URI: Optional[str] = None


class StorageSettings(BaseSettings):
    AWS_ENDPOINT_URL: Optional[AnyHttpUrl] = None
    AWS_SERVER_URL: Optional[AnyHttpUrl] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_REGION_NAME: Optional[str] = 'us-east-1'
    AWS_S3_BUCKET: str = 'signaight'
    AWS_S3_PRESIGNED_LINKS_TTL: int = 604800

    @model_validator(mode='after')
    def check_server_url_on_non_aws_s3_storage(self) -> Self:
        if (self.AWS_ENDPOINT_URL is not None
                and self.AWS_SERVER_URL is None):
            raise ValueError('Non AWS S3 storage require FQDN or IP with schema'
                             ' to provide media be externally accessible'
                             ' via AWS_SERVER_URL env variable')
        return self


class ExternalApiSettings(BaseSettings):
    EXTERNAL_PROVIDERS_ENABLED: bool = False
    NEXT_PUBLIC_MAPBOX_TOKEN: Optional[str] = None
    EPIEOS_API_KEY: Optional[str] = None
    SOCIAL_LINKS_API_KEY: Optional[str] = None
    VETRIC_FACEBOOK_API_KEY: Optional[str] = None
    VETRIC_INSTAGRAM_API_KEY: Optional[str] = None
    VETRIC_LINKEDIN_API_KEY: Optional[str] = None
    VETRIC_TWITTER_API_KEY: Optional[str] = None
    GRAYFOX_API_KEY: Optional[str] = None
    DS_APPS_BASE_URL: Optional[str] = None
    DS_APPS_API_KEY: Optional[str] = None
    FACE_COMPARE_BASE_URL: Optional[str] = None
    FACE_COMPARE_API_KEY: Optional[str] = None
    SERVICE_LOGS_BASE_URL: Optional[str] = None
    SERVICE_LOGS_API_KEY: Optional[str] = None


class JinaSettings(BaseSettings):
    JINA_REMOTE_FLOW_LINKEDIN: Optional[AnyUrl] = None
    JINA_REMOTE_EXECUTORS: bool = False
    '''
    JINA_REMOTE_EXECUTOR_WEBSEARCH: Optional[str | AnyUrl | List[AnyUrl]] = None
    @field_validator("JINA_REMOTE_EXECUTOR_WEBSEARCH", mode='before')
    def get_project_name(
        cls,
        v: str | AnyUrl | List[AnyUrl]
    ) -> AnyUrl | List[AnyUrl]:
        if not v:
            return None
        if isinstance(v, str) and ',' in v:
            v = [_v.strip() for _v in v.split(',')]
        schemas = ['grpc', 'http', 'https', 'ws', 'wss']
        if isinstance(v, list):
            v = [_v for _v in v if any(s in _v for s in schemas)]
        elif isinstance(v, str):
            v = v if any(s in v for s in schemas) else None
        return v
    '''
    JINA_KUBERNETES_MODE: bool = False
    JINA_KUBERNETES_HOSTS_SUFFIX: str = "svc.cluster.local"
    JINA_EXECUTOR_FACEBOOKAPI_REPLICAS: int = 2
    JINA_EXECUTOR_INSTAGRAMAPI_REPLICAS: int = 2
    JINA_EXECUTOR_PROFILERAPI_REPLICAS: int = 2
    JINA_EXECUTOR_WEBSCRAPER_REPLICAS: int = 5
    JINA_EXECUTOR_RESULTAPIREDUCER_REPLICAS: int = 6
    JINA_EXECUTOR_LINKEDINAPI_REPLICAS: int = 2
    JINA_EXECUTOR_PRIMARYCANDIDATEBYFACECOMPARE_REPLICAS: int = 2
    JINA_EXECUTOR_AGGREGATION_REPLICAS: int = 2


class NotificationsSettings(BaseSettings):
    SLACK_WEBHOOK_URL: Optional[AnyHttpUrl] = None


class Settings(JinaSettings,
               DatabaseSettings,
               RedisSettings,
               RabbitMQSettings,
               StorageSettings,
               ExternalApiSettings,
               NotificationsSettings,
               BaseSettings):
    DEBUG: bool = False

    ENVIRONMENT: str = 'production'

    @field_validator("ENVIRONMENT", mode='before')
    def get_project_name(cls, v: str) -> str:
        if v not in ['production', 'staging', 'development',
                     'testing', 'local']:
            v = 'local'
        return v

    # SignAIght uses one product context; the former alternate context is legacy-only.
    APP_DATA_CONTEXT: str = '50736d2841224eae663630a6ef12028ac95f4c04'
    # Secret key should based on on Fernet lib
    # and should be base64 encoded 32bytes
    SECRET: str
    ENCRYPTION_KEY: str

    '''
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @field_validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @field_validator("EMAILS_ENABLED", mode='before')
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )
    '''


settings = Settings()
