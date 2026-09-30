from beanie.odm.utils.encoder import DEFAULT_CUSTOM_ENCODERS
from pydantic import AnyHttpUrl, AnyUrl
from pymongo import AsyncMongoClient

from core.logging import logger
from core.fields import S3Path

from .config import settings

# DEFAULT_CUSTOM_ENCODERS.update({S3Path: str})
DEFAULT_CUSTOM_ENCODERS.update({
    S3Path: str,
    AnyHttpUrl: str,
    AnyUrl: str
})

client = AsyncMongoClient(
    str(settings.MONGODB_URI), uuidRepresentation="standard"
)


# NOTE: Be careful to use this decorator on functions or class
# methods with long polling actions. MongoDB has default limitation
# 30 sec for transactions timeout.
# WARNING: This value can't be changed on managed databases at MongoDB Atlas!
def with_transaction(func):
    async def wrapper(*args, **kwargs):
        try:
            async with client.start_session() as session:
                async with await session.start_transaction():
                    result = await func(*args, **kwargs, session=session)
                    return result
        except Exception as e:
            logger.error(f"Transaction failed: {str(e)}")
    return wrapper
