from functools import wraps
import traceback

from logging import getLogger
_logger = getLogger(__name__)


def async_input_entry(func):
    """Decorator. Doing nothing useful except error logging for now
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            _logger.warning(u"Exception ENTRY: '{}' '{}' '{}'".format(type(ex), ex, traceback.format_exc()))
            raise
    return wrapper
