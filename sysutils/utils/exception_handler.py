from concurrent.futures import _base
import logging

shutdown_exceptions = (GeneratorExit, _base.CancelledError)

_logger = logging.getLogger(__name__)


def check_if_exception_any_of(ex, exceptions):
    """
    Check if exception amy of from the list
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


def retry_if_exception(break_exceptions=shutdown_exceptions,
                       break_if_unknown_exception=False,
                       ignored_exception=None):

    """ Decorator
    :param ignored_exception: <exception class> exceptions will be ignored
    :return: wrapped function result
    """
    def wrap(func):
        def wrapped(*args, **kwargs):
            worker = kwargs.pop('worker_name', "IgnoreException")
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if check_if_exception_any_of(ex, break_exceptions):
                        _logger.critical('{}: exception "{}" ("{}")'.format(worker, ex, type(ex)))
                        break

                    if check_if_exception_any_of(ex, ignored_exception):
                        pass
                    else:
                        if break_if_unknown_exception:
                            _logger.critical('{}: Exception "{}" ("{}") **STOP**'.format(worker, ex, type(ex)), exc_info=True)
                            break
                        else:
                            _logger.critical('{}: Exception "{}" ("{}") SKIPPED'.format(worker, ex, type(ex)), exc_info=True)
                    continue
        return wrapped
    return wrap
