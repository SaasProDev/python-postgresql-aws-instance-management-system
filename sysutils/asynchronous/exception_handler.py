import traceback

from sysutils.asynchronous.utils import minisleep
from sysutils.asynchronous.errors import shutdown_exceptions
from sysutils.utils.reflection_utils import run_method

import logging
_logger = logging.getLogger(__name__)


class StopExecuting(Exception):
    pass


def check_if_exception_any_of(ex, exceptions):
    """
    Check if exception any of from the list
    :param ex: <Exception>
    :param exceptions: <Exception or list of ones>
    :return:
    """
    try:
        if ex and exceptions:
            exceptions_list = exceptions if isinstance(exceptions, (list, tuple)) else [exceptions]
            for e in exceptions_list:
                if issubclass(type(ex), e):
                    return True
    except:
        pass
    return False


def cycling_and_ignore_exception(func):
    async def wrapper(*args, **kwargs):
        restore_method  = kwargs.pop('restore_method', None)
        shutdown_method = kwargs.pop('shutdown_method', None)

        while True:
            try:
                await func(*args, **kwargs)
            except StopExecuting as e:
                _logger.debug('Normal stopping {}'.format(e))
                break
            except shutdown_exceptions:
                _logger.info('Shutting down ({}) {} ...'.format(type(shutdown_exceptions), shutdown_exceptions))
                if shutdown_method:
                    run_method(shutdown_method, *args, **kwargs)
                break
            except Exception as e:
                _logger.error('"{}" ("{}"); {}'.format(e, type(e), traceback.format_exc()))
                if restore_method:
                    run_method(restore_method, *args, **kwargs)
                    _logger.info("Restore method '{}' invoking...".format(restore_method))
                else:
                    await minisleep(1, name="Exception cycling timeout")
                _logger.debug("Repeating after exception {} ...".format(type(e)))
    return wrapper

