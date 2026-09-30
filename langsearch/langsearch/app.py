import asyncio
import copy
import uuid
from beanie.exceptions import DocumentNotFound
from taskiq import TaskiqEvents, TaskiqState
from pathlib import Path
#from langgraph.checkpoint.mongodb import MongoDBSaver

# WARNING: Import is important as a workaround for non dockerised app run
from langsearch.config import settings # noqa

from core.logging import logger
from langsearch.database import client as mongo_client, init_db
from langsearch.brokers import broker
from langsearch.graph import builder as graph_builder, Context
from langsearch.graph.prompts import SYSTEM_PROMPT
from langsearch.models.matcher_results import (UnifiedPerson,
    UnifiedPersonModel, ExtractedCandidate, ExtractedCandidateModel)
from langsearch.tasks import * # noqa
from langsearch.utils.graph_config import load_graph_config

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    db_initialized = False
    while not db_initialized:
        logger.info("Beanie(MongoDB) connection attempt")
        try:
            await init_db()
            db_initialized = True
        except Exception:
            await asyncio.sleep(5)
    logger.info("Beanie(MongoDB) started")

@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await mongo_client.close()
    logger.info("Beanie(MongoDB) shutdown")


@broker.task
async def search_person(
    person_id: uuid.UUID,
    flow: str,
):
    return await search_person_task(person_id, flow)
