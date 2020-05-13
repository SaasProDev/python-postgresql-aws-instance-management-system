
from django.conf.urls import url
from django.urls import path
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # url(r'^websocket/notifications/$', consumers.NotificationConsumer),
    # re_path(r'^ws/notifications/$', consumers.NotificationConsumer),
    # path('/websocket/notifications/', consumers.NotificationConsumer),
    url(r'^websocket/notifications/$', consumers.NotificationConsumer),
    # url(r'^console/$', consumers.ConsoleConsumer),
    # re_path(r'^ws/notifications/$', consumers.NotificationConsumer),
    # re_path(r'websocket/notifications/(?P<room_name>\w+)/$', consumers.NotificationConsumer),
]