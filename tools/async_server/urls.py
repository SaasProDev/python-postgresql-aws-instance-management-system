import pathlib
# from .view import home_page
# from .view import get_file
# from .view import get_favicon
from websocket_dispatcher import ws_main_handler
import settings


PROJECT_ROOT = pathlib.Path(__file__).parent

route_handlers = [

    {"route": "/ws",        "action": "GET",      "handler": ws_main_handler},
    # {"route": "/",          "action": "GET",      "handler": home_page,     "name": "home_page", "cors": settings.DEFAULT_CORS},
    # {"route": "/file/{message_uuid}",      "action": "GET",      "handler": get_file,     "name": "file_page", "cors": settings.DEFAULT_CORS},
    # {"route": "/favicon", "action": "GET", "handler": get_favicon, "name": "favicon_icon", "cors": settings.DEFAULT_CORS},

]
