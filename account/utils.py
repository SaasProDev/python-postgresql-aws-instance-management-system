from abc import ABCMeta, abstractmethod
import uuid
from functools import reduce
# from json_field import JSONField
from django.utils.functional import lazy
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


from logging import getLogger


_logger = getLogger(__name__)


DEFAULT_CACHE_TIMEOUT = settings.PERMISSION_CACHE_TIMEOUT


def get_from_cache(key):
    return cache.get(key)


def set_cache(key, value, cache_timeout=DEFAULT_CACHE_TIMEOUT):
    cache.set(key, value, cache_timeout)
    return value


def get_content_type(model):
    return ContentType.objects.get_for_model(model) if model else None


def get_selector(obj_or_model, def_app="", def_model=""):
    ctype = get_content_type(obj_or_model) if obj_or_model else None
    app_label, model_name = ctype.natural_key() if ctype else (def_app, def_model)
    return "{}.{}".format(app_label, model_name)
