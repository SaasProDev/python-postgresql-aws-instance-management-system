#!/usr/bin/env python

import sys
import asyncio
from asyncio import Queue

sys.path.append("../../")

from sysutils.asynchronous.broker.rabbitmq.rabbitmq_producer \
    import connect_params, TrivialRabbitProducer
from ahome import settings

queue = Queue()


async def reader():
    for line in sys.stdin:
        await queue.put({"line":line})
        await asyncio.sleep(0.001)


if __name__ == '__main__':
    asyncio.ensure_future(reader())
    params = connect_params(settings.RABBIT_HOST,
                            settings.RABBIT_PORT,
                            settings.RABBIT_USERNAME,
                            settings.RABBIT_PASSWORD)
    producer = TrivialRabbitProducer(params, "test", "test_rout", queue, name="CeleryLogger")
    producer.run()
    asyncio.get_event_loop().run_forever()
