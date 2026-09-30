from beanie import init_beanie
from typing import Optional

from core.logging import logger
from core.dbclient import client

from .config import MongoSrvDsn, settings
from .models import (
    UnionAuditLog,
    ProjectModel,
    PersonModel,
    AlertsModel,
    EvaluationModel,
    FlagModel,
    PersonModelAuditLog,
    CandidateModel,
    EventModel,
    SearchEventModel,
    ActiveSearchEventModel,
    RecalculationEventModel,
    WebSearchModel,
    ResourceActionLogModel,
    ServiceStepLogModel,
    AuthUserModel,
)


async def init_db(
    mongodb_uri: Optional[MongoSrvDsn] = settings.MONGODB_URI,
    allow_index_dropping: bool = False
):
    try:
        db_name = mongodb_uri.path.strip('/').split('/')[0]
    except Exception as e:
        logger.info(e)
        print("there is no database specified use default signaight")
        db_name = "signaight"
    await init_beanie(
        database=client[db_name],
        document_models=[
            CandidateModel,
            EventModel,
            PersonModel,
            AlertsModel,
            EvaluationModel,
            FlagModel,
            PersonModelAuditLog,
            ProjectModel,
            SearchEventModel,
            ActiveSearchEventModel,
            RecalculationEventModel,
            UnionAuditLog,
            WebSearchModel,
            ResourceActionLogModel,
            ServiceStepLogModel,
            AuthUserModel,
        ],
        allow_index_dropping=allow_index_dropping
    )
