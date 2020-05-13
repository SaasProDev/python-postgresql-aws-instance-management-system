import os
import asyncio
from aiohttp import web
from server import sio_server
from view import index
import settings

from logging import getLogger
from server import sio_server, sio_queue

_logger = getLogger(__name__)


from sysutils.asynchronous.web.web_server import start_web_server
from sysutils.asynchronous.web.web_server import define_routs, system_handlers

sio, app = sio_server()
mq = sio_queue()


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(5)
        count += 1
        await sio.emit('my_response', {'data': 'background_task'})
        _logger.debug("BACKGROUND_TASK")


async def rabbitmq_consumer():
    mode = os.environ.get('CURRENT_APPLICATION', "SOCKETIO.SERVER")
    if mode == "SOCKETIO.SERVER":
        from rabbit_consumer_starter import AsyncRabbitLogProxy
        AsyncRabbitLogProxy(mq).start()
        mess = "**** AsyncServer STARTED for '{}' **** ".format(mode)
    else:
        mess = "**** AsyncServer SKIPPED for '{}' **** ".format(mode)
    _logger.info(mess)

