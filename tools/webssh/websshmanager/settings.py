import os
from os import environ


def env_setting(setting, default=None):
    try:
        return environ[setting]
    except KeyError:
        print (u"### No Environ Setting for {:<20} Using default: '{}'".format(setting, default))
        return default


ENVIRONMENT_MODE = env_setting('ENVIRONMENT_MODE', 'DEVELOP').lower()

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")


TASK_TMP_ROOT = '/opt/tmp'
AHOME_PROOT_BASE_PATH = TASK_TMP_ROOT


PROXY_EXE = "/shellinabox/shellinaboxd"

# todo apply real certificate
CERTIFICATE_FOLDER = "/websshmanager"
PROXY_USER_NAME = 'root'
PROXY_GROUP_NAME = 'root'
PIDFILE_DIRECTORY = "pids"
RANDOM_PATH_LENGTH = 32
DOCUMENT_BASE = env_setting('DOCUMENT_BASE', BASE_DIR)
SHELLINABOX_ASSETS_FOLDER = "{}/shellinabox".format(DOCUMENT_BASE)


PROVIDERS_ICONS = {
    'default': 'favicon.ico'
}

SERVER_USER_PID = 0    # root
SERVER_GROUP_PID = 0   # root


PORTS_RANGE = (4199, 4399)
SERVER_PORT = 9001
EXTERNAL_PORT_NAME = 7000   # Please update nginx.conf!


WEBSSH_PROXY_BASE = env_setting('WEBSSH_PROXY_BASE', 'http://127.0.0.1:{}'.format(EXTERNAL_PORT_NAME))
CONNECT_COMMAND_TEMPLATE = WEBSSH_PROXY_BASE + "/ssh/{}{}/"

from logging.config import dictConfig
from settings_logging import get_logger_config
dictConfig(get_logger_config("webmanager.log"))


try:
    from _local_settings import *
    print("**** LOCAL SETTINGS LOADED ****")
except ImportError:
    pass
