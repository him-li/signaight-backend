import asyncio
from socketio import AsyncRedisManager as BaseAsyncRedisManager

from core.logging import logger


class AsyncRedisManager(BaseAsyncRedisManager):

    def __init__(self, url='redis://localhost:6379/0', channel='socketio',
                 write_only=False, logger=None, redis_options=None):
        super().__init__(url=url, channel=channel, write_only=write_only,
                         logger=logger, redis_options=redis_options)
        self.persistent_callbacks = {
            "user_broadcast": ["send_message_by_user_id"]
        }

    async def _handle_callback(self, message):
        # NOTE: bypass host id check in original code
        # if self.host_id == message.get('host_id'):
        try:
            sid = message['sid']
            id = message['id']
            args = message['args']
        except KeyError:
            return
        logger.info(f"{sid} | {id} | {args}")
        await self.trigger_callback(sid, id, args)

    def basic_disconnect(self, sid, namespace, **kwargs):
        if namespace not in self.rooms:
            return
        rooms = []
        for room_name, room in self.rooms[namespace].copy().items():
            if sid in room:
                rooms.append(room_name)
        for room in rooms:
            self.basic_leave_room(sid, namespace, room)
        # NOTE: avoid callback deletions if it in persistent list
        if (sid in self.callbacks
                and sid not in self.persistent_callbacks.keys()):
            del self.callbacks[sid]
        if namespace in self.pending_disconnect and \
                sid in self.pending_disconnect[namespace]:
            self.pending_disconnect[namespace].remove(sid)
            if len(self.pending_disconnect[namespace]) == 0:
                del self.pending_disconnect[namespace]

    async def trigger_callback(self, sid, id, data):
        """Invoke an application callback.

        Note: this method is a coroutine.
        """
        callback = None
        try:
            callback = self.callbacks[sid][id]
        except KeyError:
            # if we get an unknown callback we just ignore it
            self._get_logger().warning('Unknown callback received, ignoring.')
        else:
            # NOTE: avoid callback deletions if it in persistent list
            if id not in self.persistent_callbacks.get(sid, []):
                del self.callbacks[sid][id]
        if callback is not None:
            ret = callback(*data)
            if asyncio.iscoroutine(ret):
                try:
                    await ret
                except asyncio.CancelledError:  # pragma: no cover
                    pass
