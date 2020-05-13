import os, logging, socket
from os import environ
from os.path import isfile

environ['ENVIRONMENT_MODE'] = environ.get('ENVIRONMENT_MODE', '').lower() or 'develop'


def env_setting(setting, default=None):
    try:
        return os.environ[setting]
    except KeyError:
        print (u"### No Environ Setting for {:<20} Using default: '{}'".format(setting, default))
        return default


APPLICATION_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SERVICE_PORT = 3000
SERVICE_HOST = '0.0.0.0'


SERVICE_NAME = "NotificationWebServer"
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_NAME = environ.get('HOST') or socket.gethostname()

# todo reuse MAIN Django settings
RABBIT_HOST     = env_setting('RABBIT_HOST', '127.0.0.1')
RABBIT_PORT     = env_setting('RABBIT_PORT', 5672)
RABBIT_USERNAME = env_setting('RABBIT_USERNAME', 'guest')
RABBIT_PASSWORD = env_setting('RABBIT_PASSWORD', 'guest')
RABBIT_VHOST    = env_setting('RABBIT_VHOST', '/')


REDIS_HOST  = env_setting('REDIS_HOST', '127.0.0.1')
REDIS_POST  = env_setting('REDIS_PORT', 6379)
REDIS_DB    = env_setting('REDIS_DB', 0)

X_REDIS_BROKER_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_POST, REDIS_DB)

CORS_ALLOWED_ORIGINS = '*'

# CHANNEL_GROUP_NOTIFICATIONS = "notifications"
CHANNEL_GROUP_NOTIFICATIONS = "my_response"


VERBOSE = bool(__debug__)

import aiohttp_cors
DEFAULT_CORS = {
    "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*"),
}


try:
    from _local_settings import *
    print("**** LOCAL SETTINGS LOADED ****")
except ImportError:
    # print("**** SETTINGS LOADED ****")
    pass

from logging.config import dictConfig
from settings_logging import get_logger_config
dictConfig(get_logger_config("webserver.log"))
