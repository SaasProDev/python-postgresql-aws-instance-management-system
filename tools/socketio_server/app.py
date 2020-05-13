#!/usr/bin/env python

import sys
sys.path.append("../../")

from aiohttp import web
from server import sio_server
from view import index
from background_tasks import background_task, rabbitmq_consumer
import settings


from sysutils.asynchronous.web.web_server import start_web_server
from sysutils.asynchronous.web.web_server import define_routs, system_handlers

sio, app = sio_server()


default_handlers = [
    {"route": "/",        "action": "GET",      "handler": index, "name": "home"},
    {"route": "/static/", "action": "STATIC",   "path": 'static', "name": "static"},
]

if __name__ == '__main__':
    # sio.start_background_task(background_task)
    sio, app = sio_server(settings)
    define_routs(app, default_handlers + system_handlers)
    # sio.start_background_task(background_task)
    # sio.start_background_task(rabbitmq_consumer)
    # app.router.add_static('/static', 'static')
    # app.router.add_get('/', index)
    port = settings.SERVICE_PORT
    host = settings.SERVICE_HOST
    web.run_app(app, host=host, port=port)
