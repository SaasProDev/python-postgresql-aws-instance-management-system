#!/usr/bin/env python

import logging
import asyncio
import signal
import traceback

from sysutils.asynchronous.system_loop import get_main_loop
from sysutils.asynchronous.web.web_server import start_web_server
from urls import route_handlers

_logger = logging.getLogger(__name__)

import settings


def close_app(*args, **kwargs):
    _logger.info("Service {} Stopped".format(settings.SERVICE_NAME))
    pass


def shutdown_handler(loop):
    _logger.info("Stopping Service {}...".format(settings.SERVICE_NAME))
    tasks = asyncio.Task.all_tasks(loop)
    try:
        loop.stop()
        for t in tasks:
            t.cancel()
    except Exception as ex:
        _logger.debug("Exception during stopping service: {}; {}".format(ex, traceback.format_exc()))
        pass


async def empty_middleware(app, handler):
    async def middleware_handler(request):
        return await handler(request)
    return middleware_handler


def db_init(app):
    _logger.info("*** NO DATABASE CONNECT {} ***")


def queue_init(app):
    print("**** NO QUEUE Connect: '{}' ****")


def server_go(host='0.0.0.0', port=9000, handlers=route_handlers):
    loop = get_main_loop("asyncio")
    loop.add_signal_handler(signal.SIGINT, shutdown_handler, loop)
    tasks = []
    middlewares = [empty_middleware]

    def web_setup(app):
        db_init(app)
        queue_init(app)

    start_web_server(loop,
                     host=host,
                     port=port,
                     handlers=handlers,
                     tasks=tasks,
                     setup_app=web_setup,
                     close_app=close_app,
                     settings=settings,
                     heartbeat_timeout=200,
                     middlewares=middlewares)

    _logger.info("SERVICE '{}' stopped".format(settings.SERVICE_NAME))


if __name__ == "__main__":
    server_go(host="0.0.0.0", port=9000)
