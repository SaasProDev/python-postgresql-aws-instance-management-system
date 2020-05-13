"""
Something likes https://www.baeldung.com/spring-boot-actuators
"""

from aiohttp import web
from .actuator_runtime import *

import logging
_logger = logging.getLogger(__name__)


async def actuator(request):
    global STOP_MODE

    try:
        app = request.app

        param = request.match_info.get('param', "")

        if request.method == "POST":
            config = await request.json()
            if config:
                _logger.info("*** DYNAMIC CONFIGURATION UPDATE ***")
                store_data_as_config(config, app.root_folder)

        modes = {
            "config": "",
            "info": "",
            "stop": {'status': "STOPPING"},
            "restart": {'status': "RESTARTING"},
            "health": {'status': "UP"},
        }

        if param in ('stop', 'restart'):
            STOP_MODE = param.upper()
            stop_loop(app.loop)
            data = modes[param]
        elif param == "config":
            data = get_config_as_dict()
        elif param == "info":
            data = get_info(app)
        else:
            data = modes.get(param) or get_info(app)
    except Exception as ex:
        _logger.warning("Exception during ACTIVATOR executing. {}; {}".format(ex, traceback.format_exc()))
        data = {}
    return web.json_response(dict(data))
