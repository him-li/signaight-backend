import pytest
from faker import Faker
from beanie.odm.utils.init import init_beanie
from beanie.odm.utils.encoder import DEFAULT_CUSTOM_ENCODERS
from pydantic import AnyHttpUrl, AnyUrl, MongoDsn
from pymongo import AsyncMongoClient

from core.config import MongoSrvDsn
from core.models import (
    UnionAuditLog,
    ProjectModel,
    PersonModel,
    PersonModelAuditLog,
    CandidateModel,
    EventModel,
    SearchEventModel,
    ActiveSearchEventModel,
    WebSearchModel,
    AlertsModel,
    EvaluationModel,
    FlagModel
)
from core.fields import S3Path
from tests.unit.common import (
    HybridStorage,
    PictureParentDoc
)
from api.config import Settings as BaseSettings

pytest_plugins = [
    "tests.fixtures.project",
    "tests.fixtures.person",
    "tests.fixtures.candidate",
    "tests.fixtures.alerts",
    "tests.fixtures.evaluation",
    "tests.fixtures.flags",
]

# DEFAULT_CUSTOM_ENCODERS.update({S3Path: str})
DEFAULT_CUSTOM_ENCODERS.update({
    S3Path: str,
    AnyHttpUrl: str,
    AnyUrl: str
})


class Settings(BaseSettings):
    MONGODB_URI: MongoSrvDsn = "mongodb://mongodb-primary:27017/signaight-test"


@pytest.fixture(scope="module")
def fake():
    return Faker()


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture()
async def session(client):
    s = client.start_session()
    yield s
    await s.end_session()


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture()
def client(settings):
    return AsyncMongoClient(
        str(settings.MONGODB_URI),
        uuidRepresentation="standard"
    )


@pytest.fixture(autouse=True)
async def init(client, settings):
    try:
        db_name = settings.MONGODB_URI.path.strip('/').split('/')[0]
    except Exception:
        print("there is no database specified use default signaight")
        db_name = "signaight-test"

    models = [
        UnionAuditLog,
        ProjectModel,
        PersonModel,
        PersonModelAuditLog,
        CandidateModel,
        EventModel,
        SearchEventModel,
        ActiveSearchEventModel,
        HybridStorage,
        PictureParentDoc,
        WebSearchModel,
        AlertsModel,
        EvaluationModel,
        FlagModel
    ]
    await init_beanie(
        database=client[db_name],
        document_models=models,
    )

    yield None

    for model in models:
        await model.get_pymongo_collection().drop()
        await model.get_pymongo_collection().drop_indexes()
    await client.close()


@pytest.fixture(autouse=True)
def check_environment_variable(settings):
    if not settings.ENVIRONMENT == 'testing':
        pytest.fail("Unable to run tests. Env variable ENVIRONMENT"
                    " not set to 'testing' value.")
