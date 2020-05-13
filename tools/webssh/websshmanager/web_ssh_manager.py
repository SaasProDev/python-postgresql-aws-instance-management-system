import sys
import traceback

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

from pprint import pprint

sys.path.append("../")
sys.path.append("./")

import settings
from proxy_started import start_proxy, get_started_proxy

from logging import getLogger
_logger = getLogger(__name__)


class CommonHandlerMixin:
    PROXY_EXE           = settings.PROXY_EXE
    DOCUMENT_BASE       = settings.DOCUMENT_BASE
    CERTIFICATE_FOLDER = settings.CERTIFICATE_FOLDER

    def get_arg(self, param_name, default=""):
        return str(self.request.arguments.get(param_name, [bytes(default, encoding="utf-8")])[0], encoding='utf-8')


class StartHandler(RequestHandler, CommonHandlerMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        result = {"status": "ERROR"}
        try:
            webpath             = self.get_arg('path') or None
            port                = self.get_arg('port') or None
            target_host         = self.get_arg('host') or None
            target_user         = self.get_arg('user') or None
            uuid                = self.get_arg('uuid') or None
            certificate_path    = self.get_arg('cpath') or None

            data = start_proxy(target_host, target_user, port, webpath, uuid, certificate_path)

        except Exception as ex:
            _logger.warning("Cannot perform request; Exception: {}; ".format(ex, traceback.format_exc()))
        else:
            result.update({"status": "OK"})
            result.update(data)
        self.write(result)
        self.flush()


class StatusHandler(RequestHandler, CommonHandlerMixin):
    def get(self):
        infos = get_started_proxy()
        self.write({"data": infos})
        self.flush()


def make_app():
    return Application([
        url(r"/start",   StartHandler),
        url(r"/status",  StatusHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    port = int(settings.SERVER_PORT)
    app.listen(port)
    print("Serve server started. {}".format("http://localhost:{}/status".format(port)))
    IOLoop.current().start()
