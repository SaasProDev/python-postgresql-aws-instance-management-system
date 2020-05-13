"""
Something likes https://www.baeldung.com/spring-boot-actuators
"""
import os
import time
import traceback
from sysutils.asynchronous.utils import stop_loop
from sysutils.utils.debug import nice_print
from sysutils.utils.json_tools import json_write
from sysutils.utils.timeutils import display_time
import settings
import logging
_logger = logging.getLogger(__name__)

STOP_MODE = "STOP"
DYNAMIC_SETTINGS_FILENAME = "settings/settings_external.json"

try:
    SERVICE_NAME = settings.SERVICE_NAME
except:
    SERVICE_NAME = "WebApp"


def xuptime():
    import subprocess
    return subprocess.getoutput('uptime')


def uptime(start_time):
    return display_time(time.time() - start_time)


def need_restart():
    global STOP_MODE
    return STOP_MODE in ("restart", "RESTART")


def store_data_as_config(data, folder):
    filename = os.path.join(folder, DYNAMIC_SETTINGS_FILENAME)
    json_write(filename, data)
    _logger.info("Dynamic settings saved to '{}'".format(filename))


def get_config_as_dict():
    return {name: getattr(settings, name) for name in dir(settings) if name == name.upper()}


def get_start_time(app):
    try:
        return app.start_time
    except:
        return time.time()


def get_info(app):
    try:
        runner = app.get_runner(app)
        name = runner.name
    except Exception as ex:
        name = SERVICE_NAME
    return {
        "PID": os.getpid(),
        "PPID": os.getppid(),
        "ENV": os.environ.get("ENVIRONMENT_MODE"),
        "SERVICE": name,
        "UPTIME":  uptime(get_start_time(app))
    }


