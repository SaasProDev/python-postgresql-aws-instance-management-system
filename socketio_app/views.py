import logging
import threading
import time
# import eventlet
# eventlet.monkey_patch()
from django.shortcuts import render

# Create your views here.
import socketio

from logging import getLogger

_logger = getLogger(__name__)


sio = socketio.Server(async_mode='gevent_uwsgi', cors_allowed_origins=['*', 'http://127.0.0.1:8001'])

# manager = socketio.RedisManager('')
# sio = socketio.Server(client_manager=manager)


@sio.event
def connect(sid, environ):
    print('connected to ', sid)
    _logger.info( "sio: {} connected".format(sid) )
    return True


@sio.event
def disconnect(sid):
    print("disconnected", sid)
    _logger.info( "sio: {} disconnected".format(sid) )


@sio.on('chat')
def on_message(sid, data):
    print('I received a message!', data)
    sio.emit("chat", "received your msg" + str(data))
    sio.emit("chat", "welcome")

@sio.event
def bg_emit():
    print("emiitting")
    # sio.emit('chat', dict(foo='bar'))
    sio.emit('chat', data='ment')


def bkthred():
    print("strting bckgroud tsk")
    while True:
        eventlet.sleep(5)
        bg_emit()


def emit_data(data):
    print("emitting strts")
    # sio.start_background_task(target=bkthred)
    eventlet.spawn(bkthred)