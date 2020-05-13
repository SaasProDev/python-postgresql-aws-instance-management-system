import os
import logging
from django.apps import AppConfig

_logger = logging.getLogger(__name__)

modes = ["DJANGO.SERVER", "CELERY.WORKER", "DJANGO.COMMAND"]


class AsyncServerConfig(AppConfig):
    name = 'components.async_proxy'
    verbose_name = 'async_proxy worker'

    def ready(self):
        # mess = "Async Rabbit Consumer SKIPPED"
        mode = os.environ.get('CURRENT_APPLICATION', "UNDEF")
        # mode = os.environ.get('CURRENT_APPLICATION', "DJANGO.SERVER")
        if mode == "DJANGO.SERVER":
            from .async_server import AsyncServer
            AsyncServer().start()
            mess = "**** AsyncServer STARTED for '{}' **** ".format(mode)
        else:
            mess = "**** AsyncServer SKIPPED for '{}' **** ".format(mode)
        _logger.info(mess)
        # print(mess)
