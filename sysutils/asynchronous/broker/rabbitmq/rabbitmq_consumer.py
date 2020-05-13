import asyncio
import aioamqp
from aioamqp.exceptions import AmqpClosedConnection, ChannelClosed
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception

from sysutils.asynchronous.broker.rabbitmq.rabbitmq_aioampq import TrivialRabbitBrocker, connect_params
import logging


_logger = logging.getLogger(__name__)


# class TrivialRabbitConsumer(TrivialRabbitBrocker):
#     _mode = "Consumer"
#
#     def __init__(self, connect_params, queue_name=None, callback=None, **kwargs):
#         super().__init__(connect_params, **kwargs)
#         self._queue_name = queue_name
#         self._callback = callback
#
#     async def start_consuming(self, queue_name, callback, no_ack=True):
#         await self._channel.queue_declare(queue_name=queue_name)
#         await self._channel.basic_consume(callback, queue_name=queue_name, no_ack=no_ack)
#
#     async def start(self):
#         await self.start_consuming(self._queue_name, self._callback)


class TrivialRabbitConsumer(TrivialRabbitBrocker):
    _mode = "Consumer"

    def __init__(self, connect_params, queue_name, callback, **kwargs):
        super().__init__(connect_params, **kwargs)
        self._queue_name = queue_name
        self._callback = callback

    async def start_consuming(self, queue_name, callback, no_ack=True):
        await self._channel.queue_declare(queue_name=queue_name)
        await self._channel.basic_consume(callback, queue_name=queue_name, no_ack=no_ack)

    async def start(self):
        if isinstance(self._queue_name, str):
            names = [self._queue_name]
        else:
            names = self._queue_name
        for name in names:
            await self.start_consuming(name, self._callback)
