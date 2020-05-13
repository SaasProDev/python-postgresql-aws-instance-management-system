import pathlib
from view import index
import settings


PROJECT_ROOT = pathlib.Path(__file__).parent

route_handlers = [
    {"route": "/",  "action": "GET",    "handler": index,   "name": "index", "cors": settings.DEFAULT_CORS},
]
