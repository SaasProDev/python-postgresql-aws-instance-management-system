from abc import ABCMeta, abstractmethod
import asyncio
import aioamqp
from aioamqp.exceptions import AmqpClosedConnection, ChannelClosed
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception

import logging

conn_exceptions = (ConnectionError,
                   AmqpClosedConnection,
                   ChannelClosed,
                   OSError)


_logger = logging.getLogger(__name__)


def connect_params(host, port, user, password, virtualhost="/"):
    return {
        "host": host,
        "port": port,
        "login": user,
        "password": password,
        "virtualhost": virtualhost,
        "login_method": "PLAIN"
    }


class TrivialRabbitBrocker(metaclass=ABCMeta):
    _mode = "undefiend"

    PING_TIMEOUT = 1.0
    RECONNECT_TIMEOUT = 1.0
    DATA_WAIT_TIMEOUT = 0.1

    def __init__(self, connect_params, **kwargs):
        self._connect_params = connect_params
        self._transport = None
        self._protocol = None
        self._channel = None
        self._name = kwargs.pop('name', "nona name")
        self._prefetch_count = kwargs.pop('prefetch_count', None) or 1

        self._closed = False
        self.in_checking = asyncio.locks.Lock()

    @property
    def service_name(self):
        return "{}:{}".format(self._mode, self._name)

    async def connect(self):
        self._transport, self._protocol = await aioamqp.connect(**self._connect_params)
        self._channel = await self._protocol.channel()
        print("Connected [{}|{}|{}]. Service: '{}'  ".format(
            self._transport, self._protocol, self._channel, self.service_name))

    async def setup_channel(self):
        self._channel = await self._protocol.channel()
        await self._channel.basic_qos(prefetch_count=self._prefetch_count,
                                      prefetch_size=0,
                                      connection_global=False)
        _logger.debug("Chanel setup OK for '{}'".format(self.service_name))

    @abstractmethod
    async def start(self):
        """Start real work - abstractmethod """

    async def _is_protocol_connection_closed(self):
        await self._protocol.ensure_open()
        return True if not self._protocol else self._protocol.state != aioamqp.protocol.OPEN

    async def is_connection_closed(self):
        try:
            if not self._closed \
                    and self._protocol is not None \
                    and self._transport is not None \
                    and not await self._is_protocol_connection_closed() \
                    and not self._protocol.connection_closed.is_set():
                return False
            return True
        except:
            return True

    @cycling_and_ignore_exception
    async def reconnector(self, *args, **kwargs):
        # _logger.info("CONSUMER 0001 RECONNECTOR!!!")
        with await self.in_checking:
            await self.reconnect()
        await asyncio.sleep(self.RECONNECT_TIMEOUT)

    async def reconnect(self):
        # _logger.info("CONSUMER 0001 RECONNECT")
        if await self.is_connection_closed():
            _logger.debug("RabbitMQ '{}' connection closed; Reconnecting...".format(self.service_name))
            try:
                await self.connect()
                await self.setup_channel()
                await self.start()
                self._closed = False
            except conn_exceptions as e:
                _logger.critical("Failed connect to RabbitMQ '{}' will retry in {} seconds".format(
                    self.service_name, self.RECONNECT_TIMEOUT))

    @cycling_and_ignore_exception
    async def pinger(self):
        _logger.info("_heartbeat_")
        await asyncio.sleep(self.PING_TIMEOUT)

    def run(self):
        # _logger.info("CONSUMER 0000")
        asyncio.tasks.ensure_future(self.pinger())
        asyncio.tasks.ensure_future(self.reconnector())
        # _logger.info("CONSUMER 0001")
