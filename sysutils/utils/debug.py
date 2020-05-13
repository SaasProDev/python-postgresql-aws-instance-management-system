"""
copyright tretyak@gmail.com
Several methods which is useful for development/debugging
"""

import functools
import pprint


import logging
_logger = logging.getLogger(__name__)


def nice_format(data):
    return pprint.pformat(data, indent=4)


def nice_print(data):
    print(pprint.pformat(data, indent=4))


def log_trace_output(func, logger=None, message_format=None):
    """Decorator. Log result of function
    """
    logger = logger or _logger
    message_format = message_format or "{}"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            logger(message_format.format(result))
        except Exception as ex:
            _logger.warning("Cannot log output of method '{}'. Exception: {}".format(func, ex), exc_info=True)
        return result
    return wrapper
