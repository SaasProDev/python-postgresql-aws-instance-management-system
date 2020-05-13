import os
import asyncio
from django.conf import settings
from logging import getLogger

from channels.layers import get_channel_layer

from sysutils.utils.json_tools import json_loads
from pprint import pprint
from sysutils.asynchronous.broker.rabbitmq.rabbitmq_consumer import TrivialRabbitConsumer, connect_params
from sysutils.asynchronous.system_loop import start_in_thread
from sysutils.singleton import Singleton

_logger = getLogger(__name__)


try:
    CHANNEL_GROUP_NOTIFICATIONS = settings.CHANNEL_GROUP_NOTIFICATIONS
except:
    CHANNEL_GROUP_NOTIFICATIONS = "notifications"


class LogPerformer:
    """Unpack logging message and sends it to the Channel """

    MESSAGE_GROUP = CHANNEL_GROUP_NOTIFICATIONS
    MESSAGE_TYPE = "instatantlogg"

    def __init__(self):
        self._channel_layer = get_channel_layer()

    async def __call__(self, channel, body, envelope, properties):
        data = json_loads(body)
        # pprint(data, indent=4)

        await self._channel_layer.group_send(self.MESSAGE_GROUP, {
            "type": self.MESSAGE_TYPE,
            'data': data
        })


class AsyncServer(Singleton):
    """ Connect to Rabbit and consume data from the Queue """
    DEFAULT_QUEUE_NAME = "ahome.ALL"
    CELERY_QUEUE_NAME  = "ahome.CELERY.OUT"
    # QUEUE_NAME = "ahome.CELERY"
    # QUEUE_NAME = "ahome.ERROR"
    # QUEUE_NAME = "ahome.CELERY"
    # QUEUE_NAME = "ahome.INFO"

    def __init__(self):
        self._statred = False
        self._log_consumer = None

    @property
    def log_consumer(self):
        if not self._log_consumer:
            params = connect_params(settings.RABBIT_HOST,
                                    settings.RABBIT_PORT,
                                    settings.RABBIT_USERNAME,
                                    settings.RABBIT_PASSWORD,
                                    settings.RABBIT_VHOST)

            self._log_consumer = TrivialRabbitConsumer(
                params, [self.DEFAULT_QUEUE_NAME, self.CELERY_QUEUE_NAME],
                LogPerformer())
        return self._log_consumer


    def run(self):
        _logger.info("**** TrivialRabbitConsumer STARTED. QUEUES: {} ****".format([self.DEFAULT_QUEUE_NAME, self.CELERY_QUEUE_NAME]))
        self.log_consumer.run()
        from sysutils.asynchronous.socketio.client import AsyncSocketioClient
        AsyncSocketioClient(settings.SOCKETIO_SERVER).run()

    def start(self):
        if not self._statred:
            # _logger.warning("**** asyncio start_in_thread ****")
            # start_in_thread()
            self.run()

