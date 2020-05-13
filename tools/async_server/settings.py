import os, logging, socket
from os import environ
from os.path import isfile

environ['ENVIRONMENT_MODE'] = environ.get('ENVIRONMENT_MODE', '').lower() or 'develop'

try:
    from envparse import env
    if isfile('.env'):
        env.read_envfile('.env')
except:
    pass

APPLICATION_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CHECK_REGISTER_TIMEOUT = 10
# MANAGEMENT_IP = '127.0.0.1'
# MANAGEMENT_PORT = 8812

SERVICE_NAME = "WebServer"
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_HOST = environ.get('HOST') or socket.gethostname()
HOST_NAME = os.uname().nodename

VERBOSE = bool(__debug__)

LOOP = "asyncio"
TEMPLATE_ENGINE = "JINJA2"


WEBSERVER_TEMPLATE_FOLDER = [
    "{}/webapi/templates".format(APPLICATION_BASE_DIR)
]

# http configure
import aiohttp_cors
DEFAULT_CORS = {
    "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*"),
}

WEBSOCKET_HEARTBEAT_TIMEOUT_SEC = 1
#
# DB_PROPERTY_NAME = "db"
# QUEUE_PROPERTY_NAME = "nats"
#
#
# DATABASE_ENVIRONMENT = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'database': environ.get('DATABASE_NAME', 'ahome_db'),
#     'user':     environ.get('DATABASE_USER_NAME', 'ahome'),
#     'password': environ.get('DATABASE_PASSWORD', 'ahomepass123'),
#     'host':     environ.get('DATABASE_HOST') or 'postgresql',
#     'port':     environ.get('DATABASE_PORT') or '5432',
#     }
#
#
#
# DATABASE_CONNECTION_STRING = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**DATABASE_ENVIRONMENT)

# DEFAULT_NATS_HOST = "127.0.0.1"
# QUEUE_CONNECT_STRING = "nats://{}:4222".format(environ.get('NATS_HOST') or DEFAULT_NATS_HOST)
# EXTERNAL_MESSENGER_QUEUE_NAME = "external_message_queue"


from logging.config import dictConfig
from settings_logging import get_logger_config
dictConfig(get_logger_config("webserver.log"))

try:
    from _local_settings import *
    print("**** LOCAL SETTINGS LOADED")
except ImportError:
    pass
