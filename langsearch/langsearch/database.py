from beanie import init_beanie
from typing import Optional

from .config import settings

from core.logging import logger
from core.dbclient import client
from core.config import MongoSrvDsn
from langsearch.models.matcher_results import (ExtractedCandidateModel,
    UnifiedPersonModel)


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
            ExtractedCandidateModel,
            UnifiedPersonModel,
        ],
        allow_index_dropping=allow_index_dropping
    )
