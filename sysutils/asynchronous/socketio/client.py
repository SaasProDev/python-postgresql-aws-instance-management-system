import os
import socketio
import asyncio

from logging import getLogger
from sysutils.singleton import Singleton
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception

_logger = getLogger(__name__)


class AsyncSocketioClient(Singleton):
    def __init__(self, socketio_server_url):
        self._url = socketio_server_url
        self._sioclient = None

    @cycling_and_ignore_exception
    async def reconnector(self):
        if not self._sioclient:
            self._sioclient = socketio.AsyncClient()
            await self._sioclient.connect(self._url)
        await asyncio.sleep(1)
        return self._sioclient

    async def aemit(self, event_type, data):
        while not self._sioclient:
            await asyncio.sleep(1)
            print("Waiting....")
        await self._sioclient.emit("notifications", {'data': data})
        _logger.debug("SocketIO message '{}' sent. data: {}".format(event_type, data))

    def emit(self, event_type, data):
        asyncio.ensure_future(self.aemit(event_type, data))

    def run(self):
        asyncio.tasks.ensure_future(self.reconnector())
