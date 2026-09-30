import asyncio
import logging
import psutil
import os
import time
import pendulum
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_lifespan_manager import LifespanManager, State
from fastapi_pagination import add_pagination
from typing import AsyncIterator

from core.database import init_db

from api.config import settings
from api.v1.router import api_router as api_v1_router
from api.socketio import socket_manager
from tasks.brokers import broker as taskiq_broker

manager = LifespanManager()

@manager.add
async def setup_app_parts(app: FastAPI) -> AsyncIterator[State]:
    # DB init
    from core.logging import logger
    db_initialized = False
    while not db_initialized:
        try:
            await init_db(allow_index_dropping=True)
            db_initialized = True
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(5)

    # IMPORTANT: startup broker procedure before background tasks kiq after
    if not taskiq_broker.is_worker_process:
        try:
            await taskiq_broker.startup()
        except Exception as e:
            logger.error(str(e))

    yield

    # IMPORTANT: shutdown broker procedure on app close
    if not taskiq_broker.is_worker_process:
        print("Shutting down broker")
        await taskiq_broker.shutdown()


class ErrorOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            args = record.args
            if isinstance(args, tuple) and len(args) >= 5:
                status_code = args[4]  # last element in the tuple
                if status_code >= 400:
                    record.levelno = logging.ERROR
                    record.levelname = "ERROR"
        except Exception:
            pass
        return True

uvlogger = logging.getLogger("uvicorn.access").addFilter(ErrorOnlyFilter())

app = FastAPI(
        debug=settings.DEBUG,
        root_path=f"/{settings.API_PREFIX}/{settings.API_VERSION}",
        title=settings.PROJECT_NAME,
        openapi_url="/openapi.json",
        description=settings.PROJECT_NAME,
        version="0.0.2",
        default_response_class=ORJSONResponse,
        lifespan=manager,
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "persistAuthorization": True
        }
    )

# Bypass serious logging in testing mode
if not settings.ENVIRONMENT == 'testing':
    app.logger = uvlogger

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            # [str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
socket_manager.mount(app=app)


@app.get("/healthcheck")
async def read_root():
    p = psutil.Process(os.getpid())
    start = pendulum.from_timestamp(p.create_time())
    diff = pendulum.now().diff(start).in_seconds()
    return {
            "status": "OK",
            "started": start.format('YYYY-MM-DDTHH:mm:ssZ'),
            # no sence on horizontal scaled stack but ok
            "uptime": pendulum.now().subtract(seconds=diff).diff_for_humans()
        }

app.include_router(api_v1_router)

add_pagination(app)
