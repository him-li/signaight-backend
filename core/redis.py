import redis
import redis.asyncio as async_redis

from core.config import settings

redis_client = None
async_redis_client = None

def get_redis_client(async_mode=False, redis_uri=None):
    global async_redis_client
    global redis_client
    if not redis_uri:
        redis_uri = settings.REDIS_URI
    if async_mode:
        if not async_redis_client and redis_uri:
            pool = async_redis.ConnectionPool.from_url(settings.REDIS_URI)
            async_redis_client = async_redis.Redis(connection_pool=pool)
        return async_redis_client
    else:
        if not redis_client and redis_uri:
            pool = redis.ConnectionPool.from_url(settings.REDIS_URI)
            redis_client = redis.Redis(connection_pool=pool)
        return redis_client
