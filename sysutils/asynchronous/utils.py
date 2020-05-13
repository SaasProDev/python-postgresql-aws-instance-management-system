import asyncio
import async_timeout


async def minisleep(timeout=0.00001, name=None):
    """
    Sometimes very much useful for switching coroutine
    """
    await asyncio.sleep(timeout)


async def get_from_queue(output_queue, timeout=0.1):
    """
    Gets everything from internal queue and puts it in list, stops after queue being empty for some time (timeout=0.1)

    :param output_queue:
    :param timeout:
    :return: list of objects from a queue
    """
    result = []

    data = await output_queue.get()
    result.append(data)
    while True:
        try:
            with async_timeout.timeout(timeout):
                data = await output_queue.get()
                result.append(data)
        except:
            break
    return result


async def wait_completed(coroutine_or_future,  wait_timeout: float):
    try:
        with async_timeout.timeout(wait_timeout):
            return await coroutine_or_future
    except:
        raise


def stop_loop(loop):
    loop.call_soon_threadsafe(loop.stop)
