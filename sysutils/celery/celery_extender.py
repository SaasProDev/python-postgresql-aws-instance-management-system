try:
    from uuid import _uuid_generate_random
except:
    '''Fix Kombu - because '_uuid_generate_random' was removed '''
    import uuid
    uuid._uuid_generate_random = None

from celery import Celery
from celery import bootsteps
from celery.apps.worker import Worker

from logging import getLogger
_logger = getLogger(__name__)


def add_worker_channel_arguments(parser):
    parser.add_argument('--channel', type=str, default="default", help='Setup channel.')


class Bootstep(bootsteps.Step):
    def __init__(self, worker, channel="default", **options):
        print("*** CHANNEL: [{}] ***".format(channel))
        worker.app.set_channel(channel)
        super().__init__(worker, **options)


class CeleryWrapper(Celery):
    def __init__(self, name, config):
        super().__init__(name)
        self.config_from_object(config)
        self.autodiscover_tasks()


class CeleryExtender(Celery):
    def __init__(self, name, configs):
        super().__init__(name)
        self.mail_channel_name = "default"
        self.channels = {}
        self.configs = configs

        self._apply_config()

        self.user_options['worker'].add(add_worker_channel_arguments)
        self.steps['worker'].add(Bootstep)

    def set_channel(self, channel):
        self.mail_channel_name = channel
        self._apply_config()

    def _apply_config(self):
        for name, config in self.configs.items():
            if name == self.mail_channel_name:
                self.config_from_object(config)
                self.autodiscover_tasks()
            else:
                self.channels[name] = CeleryWrapper(name, config)

    def get_connector(self, name=None):
        name = name if name else self.mail_channel_name
        return super() if name == self.mail_channel_name else self.channels[name]

    def task(self, *args, **opts):
        channel = opts.pop('channel', "default")
        return self.get_connector(channel).task(*args, **opts)
