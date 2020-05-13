import os
import socketio
import random

from django.core.management.base import BaseCommand

from django.conf import settings

os.environ['CURRENT_APPLICATION'] = "DJANGO.COMMAND"

from components.socketio_client.client_connection import SocketioClient

def xsend_message():
    import random
    mq = socketio.RedisManager()
    mq.emit("my_response", {'data': "HEEEEE_LLOOOO {}".format(random.randint(100, 999))})
    mq.emit("notifications", {'data': "notifications {}".format(random.randint(100, 999))})
    sio = socketio.Client()

    sio.connect('http://localhost:8080')
    sio.emit("notifications", {'data': "XXXX notifications {}".format(random.randint(100, 999))})


def send_message():
    sio = SocketioClient('http://localhost:8080')
    # sio.emit("notifications", {'data': "CLIENTTTT notifications {}".format(random.randint(100, 999))})
    sio.emit("notifications", {'data': "****** AAAA ********"})
    sio.emit("notifications", {'data': "****** BBBB ********"})
    print("OK")


class Command(BaseCommand):
    help = 'Setup Requirement Exchanges & Queries'

    def handle(self, *args, **options):
        send_message()
        print("DONE")