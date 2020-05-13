"""
Inject asyncio loop into request
"""

from django.core.handlers.wsgi import WSGIRequest
import asyncio
#from queue import *

from django.utils.deprecation import MiddlewareMixin
from asyncio.queues import Queue
from sysutils.asynchronous.system_loop import start_in_thread
from sysutils.asynchronous.system_loop import dummy_async
from components.async_proxy.async_starter import start_async
from django.conf import settings

from sysutils.asynchronous.broker.rabbitmq.rabbitmq_aioampq import TrivialRabbitConsumer, connect_params

from django.conf import settings

from logging import getLogger
_logger = getLogger(__name__)


_loop = None
_queue = None


async def printer(channel, body, envelope, properties):
    from sysutils.utils.json_tools import json_loads
    from pprint import pprint
    try:
        data = json_loads(body)
        pprint(data, indent=4)
    except:
        pass


params = connect_params(settings.RABBIT_HOST, settings.RABBIT_PORT, settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
consumer = TrivialRabbitConsumer(params, "ahome.DEBUG", printer)


def get_loop():
    global _loop
    if not _loop:
        _loop = start_in_thread()
        start_async(dummy_async(), loop=_loop)
        _logger.info("**** EVENT LOOP STARTED ****")
    return _loop


class Publisher:
    def __init__(self):
        global _loop, _queue

        _loop = _loop or get_loop()
        _queue = _queue or Queue(loop=_loop)
        self.loop = _loop
        self.queue = _queue
        consumer.run()


from django.utils.deprecation import MiddlewareMixin


class AsyncMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        Publisher()


    def process_request(self, request):
        pass

    def process_response(self, request, response):
        return response
