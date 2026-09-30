import asyncio
import json
import redis
import random
import uuid

from rich import print
from typing_extensions import Annotated

from core.config import settings
from cli.typer_async import AsyncTyper, Argument

redis_client = redis.StrictRedis.from_url(settings.REDIS_URI)
app = AsyncTyper(no_args_is_help=True)

# python cli/app.py messages send e95224fe-5c8c-441a-a121-6340a7b54d35
@app.async_command()
async def send(
    user_id: uuid.UUID = Argument(..., help="User id"),
):
    args = [
        str(user_id),
        "Boo!"
    ]
    i=0
    while i < 100:
        redis_client.publish('socketio', json.dumps({
            "sid": "user_broadcast",
            "id": "send_message_by_user_id",
            "method": "callback",
            "args": args
        }))
        print("Message sent...")
        await asyncio.sleep(random.randint(10, 20))
        i += 1
