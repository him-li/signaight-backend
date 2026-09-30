import logging
import sys
from loguru import logger as loguru_logger

from .config import settings


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = loguru_logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class AppLogger:

    @classmethod
    def logger(cls, level="info"):
        return cls.customize_logging(
            level=level,
            format=("<level>{level: <8}</level> "
                    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
                    "request id: {extra[request_id]} - <cyan>{name}</cyan>:"
                    "<cyan>{function}</cyan> - <level>{message}</level>")
        )

    @classmethod
    def customize_logging(cls,
                          level: str,
                          format: str
                          ):

        loguru_logger.remove()
        loguru_logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        # PyMongo's DEBUG command events include complete request/reply
        # documents. Keep driver diagnostics above INFO even when the app is
        # running in debug mode so person and candidate data never reaches
        # application logs.
        for noisy_driver_logger in ("pymongo", "motor"):
            logging.getLogger(noisy_driver_logger).setLevel(logging.WARNING)
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return loguru_logger.bind(request_id=None, method=None)


'''Always import logger from here for enchanced logging.
loguru also allow to send log notifications via notifiers
library.

Usage:
    from core.logging import logger

    logger.debug("That's it, beautiful and simple logging!")
    logger.info("That's it, beautiful and simple logging!")
'''

match settings.ENVIRONMENT:
    case 'production':
        log_level = "info" if settings.DEBUG else "error"
    case 'testing':
        log_level = "critical"
    case _:
        log_level = "debug" if settings.DEBUG else "info"
logger = AppLogger.logger(level=log_level)
