"""
Start asyncio under SYNCHRONISED runtime
"""

import asyncio


from logging import getLogger
_logger = getLogger(__name__)


def start(performer, loop, *args):
    """
    Start a SYNCHRONISED function
    Run loop run_forever if loop==None

    :param performer: <function> function which will be run
    :param loop: <asyncio.loop | None>
    :param args: parameters for starting 'performer'
    :return: <asyncio.loop>
    """

    loop.run_in_executor(None, performer, *args)
    return loop


def start_async(performer, loop, *args, **kwargs):
    """
    Start a COROUTINE
    Run loop run_forever if loop==None

    :param performer: <coro_or_future> function which will be run
    :param loop: <asyncio.loop | None>
    :param args: parameters for starting 'performer'
    :param kwargs: parameters for starting 'performer'
    :return: <asyncio.loop>
    """
    asyncio.run_coroutine_threadsafe(performer, loop=loop)

