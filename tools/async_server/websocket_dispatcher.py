import traceback
import io
import time
import json
import logging
import uuid
import asyncio
import aiohttp
from aiohttp import web
from aiohttp.web import json_response

from sysutils.asynchronous.utils import minisleep
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception

import settings


from logging import getLogger
_logger = getLogger(__name__)


async def _unknown_handler(request, in_event, user_info, *args, **kwargs):
    _logger.warning("Unknown command received: {}".format(in_event))


@cycling_and_ignore_exception
async def heartbeat(ws, room_id, user, timeout):
    event_data = {"type": "heartbeat"}
    await ws.send_str(json.dumps(event_data))
    await minisleep(timeout)


def setup_heartbeat(loop, ws, room_id, user, timeout=settings.WEBSOCKET_HEARTBEAT_TIMEOUT_SEC):
    asyncio.ensure_future(heartbeat(ws, room_id, user, timeout), loop=loop)
    _logger.debug("### HEARTBEAT for User: '{}' Channel: '{}' set up".format(user, room_id))


async def test_start(request, *args, **kwargs):
    _logger.debug("TEST START")


request_performers = {
    'test':         test_start,
}


async def ws_main_handler(request):
    """
    Perform ALL WebSocket Requests

    Requests examples:
        "heartbeat"
        {"type" : "message.im", "text" :  "Hello Word", "rooms": "42e24f6c-f9a7-4958-bd39-f95926b213e5"}
    :param request:
    :return:
    """

    _logger.debug("REQUEST {} {}".format(type(request), request))


    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async def process_event(data_str_or_event, binary_data=None):
        try:
            event = data_str_or_event if isinstance(data_str_or_event, dict) else json.loads(data_str_or_event)

        except Exception as e:
            _logger.error("NOT JSON: '{}'. {}; {}".format(data_str, e, traceback.format_exc()))
            return
        else:
            _logger.debug("#### GOT MESSAGE '{}'; Processing it...".format(event))

        handler = request_performers.get(event['type']) or _unknown_handler

        await handler(ws, request, event)


    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                marker = "#####XJSB"
                json_size_size = 6
                bytedata = getattr(msg, 'data', b'')
                reader = io.BytesIO(bytedata)
                header = reader.read(len(marker)).decode(encoding="ascii")

                if header == 'heartbeat':
                    await ws.send_str('heartbeat')
                    continue

                if header == marker:
                    json_size = int(reader.read(json_size_size).decode(encoding="ascii"))
                    data_str = reader.read(json_size).decode(encoding="utf-8")
                    data = json.loads(data_str)
                    binary_payload = reader.read()
                    await process_event(data, binary_payload)
                continue

            if msg.type == aiohttp.WSMsgType.TEXT:
                data_str = getattr(msg, 'data', '').strip()
                if len(data_str) > 0:
                    if msg.data == 'heartbeat':
                        await ws.send_str('heartbeat')
                    else:
                        await process_event(data_str)
                else:
                    _logger.warning("Empty TEXT WS request")
                    pass

    except asyncio.CancelledError:
        _logger.info("WS Disconnected")
    except Exception as e:
        _logger.error("****** Exception: {}; {} ".format(e, traceback.format_exc()))
    finally:
        _logger.info("WS Closed")

    return ws
