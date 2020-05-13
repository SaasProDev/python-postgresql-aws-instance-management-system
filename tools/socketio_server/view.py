import asyncio
from aiohttp import web
from logging import getLogger
from server import sio_server
import settings

_logger = getLogger(__name__)

sio, app = sio_server(settings)


async def index(request):
    with open('app.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('test_event')
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data'] + "  ... TEST"}, room=sid)
    print("**** RESEIVED ****")
    print("**** RESEIVED ****")
    print("**** RESEIVED ****")
    print("**** RESEIVED ****")
    print("**** RESEIVED ****")
    _logger.debug("Receive event '{}'".format('test_event'))


@sio.on('notification', namespace='/notifications')
# @sio.on('notification')
async def my_notifications(sid, message):
    _logger.debug("**** RECEIVE NOTIFICATIONS EVENT **** '{}/{}'".format(sid, message))
    await sio.emit('hwhwhwhw', {'data': "HAAAAA_HAAAAA"}, room=sid)
    await sio.emit('notification', {'data': "TTTTTTT"}, room=sid)
    await sio.emit('notifications/notification', {'data': "DDDDDD"}, room=sid)
    await sio.emit('/notifications/notification', {'data': "NNNNNN"}, room=sid)
    # await sio.emit('notifications/notification', {'data': message['data'] + "  ... notification1"}, room=sid)
    # await sio.emit('/notifications/notification', {'data': message['data'] + "  ... notification2"}, room=sid)
    await sio.emit('my_response', {'data': "RRRRRR1"}, room=sid)
    await sio.emit('notifications/my_response', {'data': "RRRRRR2"}, room=sid)
    await sio.emit('/notifications/my_response', {'data': "RRRRRR3"}, room=sid)

@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)
