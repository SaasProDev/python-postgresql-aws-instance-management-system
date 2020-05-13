#!/usr/bin/env python

from aiohttp import web
import socketio
import logging

_logger = logging.getLogger(__name__)

__all__ = ['sio_server', 'sio_queue']

sio, app, mq = None, None, None


def parameter(settings, name, default):
    return getattr(settings, name) if hasattr(settings, name) else default


def allowed_hosts(settings):
    return parameter(settings, 'CORS_ALLOWED_ORIGINS', None)


def _server_init(settings=None):
    global sio, app, mq
    redis_url = parameter(settings, 'REDIS_BROKER_URL', None)
    if not sio:
        _logger.info("Redis Broker: '{}' CONNECTING...".format(redis_url))
        mq = socketio.AsyncRedisManager(redis_url) if redis_url else None

        params = {
            'async_mode': 'aiohttp',
            'cors_allowed_origins': allowed_hosts(settings),
            'client_manager': mq
        }
        # if mq:
        #     params['client_manager'] = mq

        sio = socketio.AsyncServer(**params)
        app = web.Application()
        sio.attach(app)
    return sio, app, mq


def sio_server(settings=None):
    sio, app, mq = _server_init(settings)
    return sio, app


def sio_queue(settings=None):
    sio, app, mq = _server_init(settings)
    return mq
