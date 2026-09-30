import json
import redis

from .config import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URI)

def send_notification(*args):
    redis_client.publish('socketio', json.dumps({
        "sid": "user_broadcast",
        "id": "send_message_by_user_id",
        "method": "callback",
        "args": args
    }))
