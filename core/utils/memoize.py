from functools import wraps
from django.utils.text import slugify


def get_memoize_cache():
    from django.core.cache import cache
    return cache


def memoize_delete(function_name):
    cache = get_memoize_cache()
    return cache.delete(function_name)


def memoize(ttl=60, cache_key=None, track_function=False, cache=None):
    """
    Decorator to wrap a function and cache its result.
    """
    if cache_key and track_function:
        raise Exception("Can not specify cache_key when track_function is True")
    cache = cache or get_memoize_cache()

    def memoize_decorator(f):
        @wraps(f)
        def _memoizer(*args, **kwargs):
            if track_function:
                cache_dict_key = slugify('%r %r' % (args, kwargs))
                key = slugify("%s" % f.__name__)
                cache_dict = cache.get(key) or dict()
                if cache_dict_key not in cache_dict:
                    value = f(*args, **kwargs)
                    cache_dict[cache_dict_key] = value
                    cache.set(key, cache_dict, ttl)
                else:
                    value = cache_dict[cache_dict_key]
            else:
                key = cache_key or slugify('%s %r %r' % (f.__name__, args, kwargs))
                value = cache.get(key)
                if value is None:
                    value = f(*args, **kwargs)
                    cache.set(key, value, ttl)

            return value

        return _memoizer

    return memoize_decorator
