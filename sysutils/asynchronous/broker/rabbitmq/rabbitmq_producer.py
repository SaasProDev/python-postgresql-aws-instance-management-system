import asyncio
import asyncio.tasks
import aioamqp
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception
from sysutils.utils.json_tools import json_dumps
from sysutils.asynchronous.broker.rabbitmq.rabbitmq_aioampq import TrivialRabbitBrocker, connect_params
import logging


_logger = logging.getLogger(__name__)


class TrivialRabbitProducer(TrivialRabbitBrocker):
    _mode = "Producer"

    def __init__(self, connect_params, exchange_name, routing_key, queue, **kwargs):
        super().__init__(connect_params, **kwargs)
        self._exchange_name = exchange_name
        self._internal_queue = queue
        self._routing_key = routing_key

    async def setup_exchange(self, exchange_name, exchange_type='direct'):
        await self._channel.exchange_declare(exchange_name=exchange_name, exchange_type=exchange_type)

    async def publish_message(self, message, routing_key):
        if not message:
            _logger.debug("*** EMPTY message to RabbitMQ. SKIPPED ***")
            return True
        # _logger.debug("*** Put message to RabbitMQ. Service: '{}' Exchange: '{}' .. <{}>".format(
        #     self.service_name, self._exchange_name, str(message)[:100]))

        if await self.is_connection_closed():
            _logger.warning("Cannot put message into a closed channel.  SKIPPED.")
            return False
        try:
            await self._channel.basic_publish(
                payload=message,
                exchange_name=self._exchange_name,
                routing_key=routing_key
            )
        except aioamqp.exceptions.ChannelClosed:
            _logger.warning("Connection closed.")
            self._closed = True
            return False

        return True

    @cycling_and_ignore_exception
    async def producer(self, *args, **kwargs):
        if await self.is_connection_closed():
            return await asyncio.sleep(self.RECONNECT_TIMEOUT)

        if self._internal_queue.qsize() == 0:
            return await asyncio.sleep(self.DATA_WAIT_TIMEOUT)

        data = await self._internal_queue.get()
        if data:
            message = json_dumps(data, ensure_ascii=False)
            while not await self.publish_message(message, self._routing_key):
                await asyncio.sleep(self.RECONNECT_TIMEOUT / 2)
        await asyncio.sleep(0.0001)


    async def start_producing(self):
        # await self.setup_exchange()
        asyncio.tasks.ensure_future(self.producer())

    async def start(self):
        await self.start_producing()

#
# from asyncio import Queue
# queue = Queue()
# i = 0
#
# def data_generator():
#     from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception, StopExecuting
#     @cycling_and_ignore_exception
#     async def test():
#         global i
#         global queue
#         i += 1
#         mess = {"test": "OK {}".format(i)}
#         print(mess)
#         await queue.put(mess)
#         await asyncio.sleep(0.1)
#     return test()
#
#
# def env_setting(setting, default=None):
#     import os
#     try:
#         return os.environ[setting]
#     except KeyError:
#         print (u"### No Environ Setting for {:<20} Using default: '{}'".format(setting, default))
#         return default
#
#
# RABBIT_HOST     = env_setting('RABBIT_HOST', '127.0.0.1')
# RABBIT_PORT     = env_setting('RABBIT_PORT', 5672)
# RABBIT_USERNAME = env_setting('RABBIT_USERNAME', 'guest')
# RABBIT_PASSWORD = env_setting('RABBIT_PASSWORD', 'guest')
# RABBIT_VHOST    = env_setting('RABBIT_VHOST', '/')
#
#
#
# def main():
#     loop = asyncio.get_event_loop()
#     params = connect_params(RABBIT_HOST, RABBIT_PORT, RABBIT_USERNAME, RABBIT_PASSWORD)
#     producer = TrivialRabbitProducer(params, "test", "test_rout", queue, name="tester")
#     producer.run()
#     asyncio.ensure_future(data_generator())
#     loop.run_forever()
#
#
# if __name__ == "__main__":
#     main()

# https://khashtamov.com/ru/django-channels-websocket/