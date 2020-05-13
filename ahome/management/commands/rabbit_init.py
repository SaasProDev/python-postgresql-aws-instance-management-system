import copy
import sys
import traceback
import pika
from attrdict import AttrDict
from django.core.management.base import BaseCommand

from django.conf import settings


DEFAULT_RABBIT_QUERIES = [
    AttrDict({"exchange": "ahome.server",  "type": "topic", "durable": True,
              "queries": [
                    AttrDict({"name": "ahome.CELERY.OUT", "routing_key": "celery.out"}),
                    AttrDict({"name": "ahome.CELERT", "routing_key": "celerytask.*"}),
                    AttrDict({"name": "ahome.CELERY", "routing_key": "celery.*"}),
                    AttrDict({"name": "ahome.WARN",   "routing_key": "*.warning"}),
                    AttrDict({"name": "ahome.ERROR",  "routing_key": "*.error"}),
                    AttrDict({"name": "ahome.INFO",   "routing_key": "*.info"}),
                    AttrDict({"name": "ahome.DEBUG",  "routing_key": "*.debug"}),
                    AttrDict({"name": "ahome.ALL",    "routing_key": "*.*"}),
              ]}),
]


def get_credentials():
    host = settings.RABBIT_HOST
    port = settings.RABBIT_PORT
    vhost = settings.RABBIT_VHOST
    password = settings.RABBIT_PASSWORD
    user = settings.RABBIT_USERNAME
    credentials = pika.PlainCredentials(user, password)
    params = pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials)
    return params


def create_exchanges():
    credentials = get_credentials()
    connection = pika.BlockingConnection(credentials)
    channel = connection.channel()

    for item in DEFAULT_RABBIT_QUERIES:
        exchange_name = item.exchange
        exchange_type = item.type
        durable = item.durable
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)

        for query in item.queries:
            queue_name = query.name
            routing_key = query.routing_key
            channel.queue_declare(queue=queue_name)
            channel.queue_bind(queue_name, exchange_name, routing_key)
            print("Rabbit Queue '{}' CREATED and bound to '{}' routing_key: '{}'".format(queue_name, exchange_name, routing_key))


class Command(BaseCommand):
    help = 'Setup Requirement Exchanges & Queries'

    def handle(self, *args, **options):
        create_exchanges()
