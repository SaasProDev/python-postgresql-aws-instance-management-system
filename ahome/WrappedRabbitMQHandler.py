import time
import pika
from python_logging_rabbitmq import RabbitMQHandlerOneWay


class RabbitLogger(RabbitMQHandlerOneWay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def message_worker(self):
        record, routing_key = None, None
        while 1:
            try:
                if record is None:
                    record, routing_key = self.queue.get()

                if     not self.channel \
                    or not self.connection \
                    or self.connection.is_closed \
                    or not self.channel \
                    or self.channel.is_closed:

                    # print("CONNECTING....")
                    self.open_connection()

                    time.sleep(1)

                self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=routing_key,
                    body=record,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        headers=self.message_headers
                    )
                )
                record, routing_key = None, None

            except Exception:
                self.channel, self.connection = None, None
                # print("Exception. SKIPPED. WILL BE REPEATED.")
            else:
                self.queue.task_done()
                if self.close_after_emit:
                    self.close_connection()