#!/usr/bin/env python

import os
import sys
import fcntl
import subprocess
import asyncio
from asyncio import Queue

sys.path.append("./")


from sysutils.asynchronous.broker.rabbitmq.rabbitmq_producer \
    import connect_params, TrivialRabbitProducer

from ahome import settings

queue = Queue()

# CELERY_WORKER_COMMAND = ['celery', 'worker', '-A', 'ahome', '-l', 'debug']
CELERY_WORKER_COMMAND = settings.CELERY_WORKER_COMMAND


def turn_to_unblocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


async def process_line(line, name="stdout"):
    if line:
        line = line[:-1]
        print(str(line, encoding='utf-8'), sep="")
        await queue.put({'module': "CELERY.OUT", name: line})


async def start_celery():
    args = CELERY_WORKER_COMMAND
    print("STARTING... >> {}".format(" ".join(args)))

    with subprocess.Popen(args,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE
                          ) as proc:

        turn_to_unblocking(proc.stdout)
        turn_to_unblocking(proc.stderr)

        while True:
            await process_line(proc.stdout.readline(), "stdout")
            await process_line(proc.stderr.readline(), "stderr")
            await asyncio.sleep(0.001)


if __name__ == '__main__':
    os.environ["CURRENT_APPLICATION"] = "CELERY.WORKER"

    params = connect_params(settings.RABBIT_HOST,
                            settings.RABBIT_PORT,
                            settings.RABBIT_USERNAME,
                            settings.RABBIT_PASSWORD)

    producer = TrivialRabbitProducer(params,
                                     "ahome.server",
                                     "celery.out",
                                     queue,
                                     name="CeleryLogger")
    producer.run()
    asyncio.ensure_future(start_celery())
    asyncio.get_event_loop().run_forever()
