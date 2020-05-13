import asyncio
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception
from threading import Thread

from logging import getLogger
_logger = getLogger(__name__)


def uvloop_loop():
    import uvloop
    return uvloop.new_event_loop()


def get_main_loop(loop_name=None):
    loop_name = loop_name or "default"
    if loop_name == 'uvloop':
        loop = uvloop_loop()
    else:
        loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def create_main_loop(loop_name=None):
    loop_name = loop_name or "default"
    if loop_name == 'uvloop':
        loop = uvloop_loop()
    else:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def start_in_thread(loop_name=None):
    loop = create_main_loop(loop_name)

    def run_forever(loop):
        loop.run_forever()

    thread = Thread(target=run_forever, args=(loop,))
    thread.start()

    _logger.debug("Asyncio in Thread started")

    return loop


@cycling_and_ignore_exception
async def dummy_async():
    await asyncio.sleep(0.1)
