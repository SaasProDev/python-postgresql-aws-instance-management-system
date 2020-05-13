import os
import socketio
from django.conf import settings
from logging import getLogger
from sysutils.singleton import Singleton

_logger = getLogger(__name__)


try:
    CHANNEL_GROUP_NOTIFICATIONS = settings.CHANNEL_GROUP_NOTIFICATIONS
except:
    CHANNEL_GROUP_NOTIFICATIONS = "notifications"


class SocketioClient(Singleton):
    def __init__(self, socketio_server_url):
        self._url = socketio_server_url
        self._sioclient = None

    @property
    def sio(self):
        if not self._sioclient:
            self._sioclient = socketio.Client()
            self._sioclient.connect(self._url)
        return self._sioclient

    def emit(self, event_type, data):
        self.sio.emit("notifications", {'data': data})
        _logger.debug("SocketIO message '{}' sent. data: {}".format(event_type, data))
