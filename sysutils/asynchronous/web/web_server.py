"""
Base web server
Supposes 'settings' project-wide defined

@see http://aiohttp.readthedocs.io/en/v0.12.0/web.html

"""
import copy
import signal
import asyncio
from aiohttp import web
import aiohttp_cors
import time
import functools
from sysutils.asynchronous.web.server import run_app
from sysutils.utils.file_utils import read_text_file, is_file_exists
from sysutils.asynchronous.exception_handler import cycling_and_ignore_exception
from sysutils.asynchronous.utils import minisleep
from sysutils.utils.debug import nice_format

from .actuator.actuator import actuator

import settings

import logging
_logger = logging.getLogger(__name__)

DEBUG = bool(__debug__)

try:
    SERVICE_NAME = settings.SERVICE_NAME
except:
    SERVICE_NAME = "WebApp"


async def dummy_home_page(request):
    app = request.app
    return web.Response(text="{} works".format(SERVICE_NAME))


async def dummy_json(request):
    app = request.app
    data = {'app': '{}'.format(app)}
    return web.json_response(data)


async def check_register(request):
    """
    Register EXTERNAL Application/Service
    :param request:
    :return: <Json>
    """
    from aiohttp import web
    data = await request.post() or {"TEST": "OK"}
    _logger.debug("CHECK_REGISTER. Data: {}".format(nice_format(data)))
    return web.json_response(data)


CORS_ALLOW_ALL = {
    "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*"),
    }

DEFAULT_CORS = {
    "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*"),
    }

default_handlers = [
    {"route": "/",        "action": "GET",      "handler": dummy_home_page, "name": "home"},
    {"route": "/json/",   "action": "GET",      "handler": dummy_json,      "name": "json"},
    {"route": "/static/", "action": "STATIC",   "path": 'static',           "name": "static"},
]

system_handlers = [
    {"route": "/static/", "action": "STATIC", "path": 'webapi/static', "name": "static"},
    {"route": "/actuator", "action": "GET", "handler": actuator, "name": "actuator_base"},
    {"route": "/actuator/{param}", "action": "GET",  "handler": actuator, "name": "actuator"},
    {"route": "/actuator/{param}", "action": "POST", "handler": actuator, "name": "actuator_update"},
    {"route": "/check_register/", "action": "POST", "handler": check_register, "name": "check_register"},

]


def adjust_handlers(handlers):
    root = [x for x in handlers if x["route"] == "/"]
    actuator = [x for x in handlers if x["route"] == "/actuator"]
    if root:
        return
    if actuator:
        actuator = copy.deepcopy(actuator[0])
        actuator["route"] = "/"
        actuator["name"] = "actuator_auto"
        handlers.append(actuator)
        _logger.debug("Actuator bind to '/'")


def print_handlers(handlers):
    print("Handlers:")
    for h in handlers:
        print("{:>8}::{}".format(h['action'], h['route']))


def define_cors(app, defaults=None):
    """
    See https://github.com/aio-libs/aiohttp-cors#usage
    :param app:
    """
    app.cors = aiohttp_cors.setup(app, defaults=defaults)


def define_routs(app, handlers=None, actuator=None):
    try:
        from routes import setup_routes
        setup_routes(app)
        _logger.info("Routes defined by external file")
    except:
        _logger.info("No external defined routes")
        pass

    handlers = handlers or []

    for handler in handlers:
        if handler.get("action", "").upper() == "POST":
            route = app.router.add_post(handler["route"], handler["handler"], name=handler.get("name", None))
            cors = handler.get("cors")
            if cors:
                app.cors.add(route, cors)
        elif handler.get("action", "").upper() == "GET":
            if actuator and handler.get("name", "") == "actuator":
                handler["handler"] = actuator
            app.router.add_get(handler["route"], handler["handler"], name=handler.get("name", None))
        elif handler.get("action", "").upper() == "STATIC":
            try:
                route = handler.get('route', '/static/')
                app.router.add_static(route, path=handler["path"], name=handler.get("name", None))
            except ValueError as err:
                _logger.debug("Static directory not defined. SKIPPED")
        else:
            pass


def define_middlewares(app):
    try:
        from middlewares import setup_middlewares
        setup_middlewares(app)
        _logger.info("Middlewares defined by external file")
    except:
        _logger.info("No external defined middlewares")
        pass


def define_template_engine(app, settings):
    if settings.TEMPLATE_ENGINE.upper() == "MAKO":
        import aiohttp_mako
        aiohttp_mako.setup(app, directories=["webapi/templates_mako"])
        app.template_seek_folders = [] # Do NOT Implemented yet
        _logger.info("Template Engine: 'MAKO'")
    elif settings.TEMPLATE_ENGINE.upper() == "JINJA2":
        import jinja2
        import aiohttp_jinja2
        seek_folders = settings.WEBSERVER_TEMPLATE_FOLDER
        app.template_seek_folders = seek_folders
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(seek_folders))
        _logger.info("Template Engine: 'JINJA2'")
    else:
        _logger.info("Template Engine Not Defined")
        pass


def unpack_as_internal_template(str):
    tmp = []
    for i in range(len(str)):
        ch = str[i]
        if ch in ['\n', '\r']:
            tmp.append(" ")
            continue
        if ch == '"':
            tmp.append('\\"')
            continue
        tmp.append(ch)
    return "".join(tmp)


def internal_template(app, template_name):
    template_file = template_name if template_name.find(".") != -1 else template_name + ".html"
    for folder in app.template_seek_folders:
        if is_file_exists(template_file, folder):
            template_str = read_text_file(template_file, folder)
            return unpack_as_internal_template(template_str)
    return ""


def default_close_app(*args, **kwargs):
    _logger.info("Web Server Stopping...")

    async def stop():
        _logger.info("WEB SERVER STOPPED")
        pass

    return asyncio.ensure_future(stop())


def default_shutdown_handler(*args, **kwargs):
    _logger.info("Web Server Shut Down...")


def default_setup_app(app, *args, **kwargs):
    _logger.info("Any additional Web Server setup")
    pass


def default_check_app(app, data=None, *args, **kwargs):
    # _logger.debug("No special checking. STATUS: {}".format(nice_format(data)))
    pass


def get_runner(app):
    if hasattr(app, "runner"):
        return app.runner
    if hasattr(app, "manager"):
        return app.manager
    return None


def create_shutdown_handler(func, loop, app, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(loop, app, *args, **kwargs)
    return wrapper


def start_web_server(loop=None,
                     host='0.0.0.0',
                     port=8080,
                     handlers=default_handlers,
                     tasks=None,
                     setup_app=default_setup_app,
                     close_app=default_close_app,
                     check_app=default_check_app,
                     shutdown_handler=default_shutdown_handler,
                     middlewares=None,
                     actuator=None,
                     **kwargs):

    _logger.info("SERVICE '{}' started".format(SERVICE_NAME))
    # loop = loop or get_main_loop()
    loop = asyncio.get_event_loop()
    # see https://docs.aiohttp.org/en/stable/web_reference.html#application-and-router
    app = web.Application(loop=loop, logger=_logger, debug=DEBUG, middlewares=middlewares or [])
    app.start_time = time.time()
    app.get_runner = get_runner

    handlers += system_handlers
    adjust_handlers(handlers)

    define_cors(app)
    define_routs(app, handlers, actuator)
    define_middlewares(app)
    #define_template_engine(app, settings)

    app.on_cleanup.append(close_app)

    if shutdown_handler:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, create_shutdown_handler(shutdown_handler, loop, app), loop)

    try:
        if settings.DEBUG_TOOLBAR:
            import aiohttp_debugtoolbar
            aiohttp_debugtoolbar.setup(app)
    except:
        pass

    setup_app(app)
    app.check_app = check_app

    print_handlers(handlers)

    run_app(app, host=host, port=port, tasks=tasks)
    _logger.info("SERVICE '{}' stopped".format(SERVICE_NAME))
    return app
