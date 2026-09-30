import socketio
import uuid

from fastapi import FastAPI
from typing import Union

from core.socketio import AsyncRedisManager
from core.logging import logger

from api.auth import get_socket_user_id
from api.config import settings

class SocketManager:

    def __init__(
        self,
        app: FastAPI = None,
        socketio_path: str = "/ws/socket.io",
        cors_allowed_origins: Union[str, list] = '*',
        async_mode: str = "asgi",
        **kwargs
    ) -> None:
        mgr = AsyncRedisManager(
            settings.REDIS_URI,
            channel='socketio',
            logger=logger
        )
        mgr.callbacks = {
            "user_broadcast": {
                "send_message_by_user_id": self.send_message_by_user_id
            }
        }
        # TODO: Change Cors policy based on fastapi cors Middleware
        self._sio = socketio.AsyncServer(
            async_mode=async_mode,
            cors_allowed_origins=cors_allowed_origins,
            auto_connect=False,
            client_manager=mgr,
            **kwargs
        )
        self._app = socketio.ASGIApp(
            socketio_server=self._sio,
            socketio_path=socketio_path
        )
        if app:
            self.mount(app, socketio_path)

        self.clients = {}

    def mount(
        self,
        app: FastAPI = None,
        socketio_path: str = "/ws/socket.io",
    ):
        app.mount(socketio_path, self._app)
        app.sio = self._sio

    def is_asyncio_based(self) -> bool:
        return True

    @property
    def on(self):
        return self._sio.on

    @property
    def attach(self):
        return self._sio.attach

    @property
    def emit(self):
        return self._sio.emit

    @property
    def send(self):
        return self._sio.send

    @property
    def call(self):
        return self._sio.call

    @property
    def close_room(self):
        return self._sio.close_room

    @property
    def get_session(self):
        return self._sio.get_session

    @property
    def save_session(self):
        return self._sio.save_session

    @property
    def session(self):
        return self._sio.session

    @property
    def disconnect(self):
        return self._sio.disconnect

    @property
    def handle_request(self):
        return self._sio.handle_request

    @property
    def start_background_task(self):
        return self._sio.start_background_task

    @property
    def sleep(self):
        return self._sio.sleep

    @property
    def enter_room(self):
        return self._sio.enter_room

    @property
    def leave_room(self):
        return self._sio.leave_room
    
    @property
    def register_namespace(self):
        return self._sio.register_namespace

    async def add_client(self, user_id, sid):
        if user_id not in self.clients:
            self.clients[user_id] = []
        self.clients[user_id].append(sid)
        logger.info(f"Session {sid} for user id {user_id} registered")

    async def remove_client(self, sid):
        '''
        try:
            print(self._sio.get_environ(sid))
            token = (self._sio
                     .get_environ(sid).get("HTTP_COOKIE", "")
                     .split(';')[0]
                     .split('=')[1])
            user_id = await get_socket_user_id(token)
            if user_id in self.clients:
                self.clients.get(user_id,
                        []).pop(self.clients[user_id].index(sid), None)
                logger.info(
                    f"Session {sid} for user id {user_id} deregistered")
        except Exception as e:
            logger.info(e)
        '''
        for user_id, sids in self.clients.items():
            if sid in sids:
                try:
                    del self.clients[user_id][sids.index(sid)]
                    logger.info(
                        f"Session {sid} for user id {user_id} deregistered")
                except Exception as e:
                    logger.info(e)

    def get_client_sids(self, user_id):
        logger.info(self.clients)
        if user_id in self.clients:
            return self.clients.get(user_id, [])
        else:
            return None

    async def send_message_by_user_id(self, user_id, message):
        if isinstance(user_id, str):
            try:
                user_id = uuid.UUID(user_id)
            except:
                return
        sid = self.get_client_sids(user_id)
        if (sid):
            await self.send({"message": message}, room=sid)


socket_manager = SocketManager()

@socket_manager.on('connect')
async def handle_connect(sid, environ, token):
    user_id = await get_socket_user_id(token)
    await socket_manager.add_client(user_id, sid)


@socket_manager.on('disconnect')
async def handle_disconnect(sid):
    await socket_manager.remove_client(sid)


@socket_manager.on('message')
def handle_message(sid, data):
    pass
