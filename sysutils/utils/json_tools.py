import json
import datetime
import decimal
import uuid
import six
import collections

from functools import wraps
from logging import getLogger
_logger = getLogger(__name__)

JsonDecodeError = (json.JSONDecodeError, TypeError)


class ExtendedJSONDecoder(json.JSONDecoder):
    from json.decoder import WHITESPACE
    def decode(self, s, _w=WHITESPACE.match):
        # print("INPUT OBJECT **** : [{}] {}".format(type(s), s))
        obj = super().decode(s, _w)
        # print("REAL OBJECT ***** : [{}] {}".format(type(obj), obj))
        return obj


class ExtendedJsonEncoder(json.JSONEncoder):
    """
    Based on REST Framework JSONEncoder
    .venv/lib/python3.7/site-packages/rest_framework/utils/encoders.py
    """

    def default(self, obj):
        #from sysutils.celery.task import AsyncTask
        try:
            if isinstance(obj, datetime.datetime):
                representation = obj.isoformat()
                if representation.endswith('+00:00'):
                    representation = representation[:-6] + 'Z'
                return representation
            elif isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, datetime.time):
                return obj.isoformat()
            elif isinstance(obj, datetime.timedelta):
                return six.text_type(obj.total_seconds())
            elif isinstance(obj, decimal.Decimal):
                return float(obj)
            elif isinstance(obj, uuid.UUID):
                return six.text_type(obj)
            elif isinstance(obj, collections.OrderedDict):
                return tuple(obj)
            elif isinstance(obj, collections.Set):
                return tuple(obj)
            elif isinstance(obj, bytes):
                return obj.decode('utf-8')
            elif hasattr(obj, 'tolist'):
                return obj.tolist()     # Numpy arrays and array scalars.
            elif hasattr(obj, '__getitem__'):
                return dict(obj)
            elif hasattr(obj, '__iter__'):
                return tuple(item for item in obj)
            #elif isinstance(obj, AsyncTask):
            #    return obj.__xdict__
            return super().default(obj)
        except Exception as ex:
            _logger.error("Cannot provide JSON decoding. EX: type: {} obj: {} Ex: {}".format(type(obj), obj, ex))
            return str(obj)


def json_dumps_extended(data: [list, dict], **kwargs) -> str:
    return json_dumps(data, cls=ExtendedJsonEncoder, **kwargs)


def json_loads_extended(data_as_string: str, **kwargs) -> [list, dict]:
    return json_loads(data_as_string, cls=ExtendedJSONDecoder, **kwargs)


class BytesFixJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode(encoding='utf-8')
        else:
            return super().default(obj)



def json_dumps(data, *args, **kwargs):
    """
    JSON encoding fixer
    """
    cls = kwargs.pop('cls', None) or BytesFixJsonEncoder
    return json.dumps(data, cls=cls, *args, **kwargs)


def json_loads(data_as_string, *args, **kwargs):
    if data_as_string:
        if isinstance(data_as_string, bytes):
            data_as_string = data_as_string.decode(encoding='utf-8')
        return json.loads(data_as_string, *args, **kwargs)


def bytes_fix_encoder(obj):
    if isinstance(obj, bytes):
        return obj.decode(encoding='utf-8')
    return obj

# todo only for copy/paste
def json_file(filename, *args, **kwargs):
    with open(filename, "rb") as fh:
        data_as_string = fh.read()
        if isinstance(data_as_string, bytes):
            data_as_string = data_as_string.decode('utf-8', 'ignore')
        return json.loads(data_as_string, *args, **kwargs)


def json_write(filename, data, dumper=ExtendedJsonEncoder):
    """
    Write data to json file
    :param filename: <str> Filename data storing
    :param data: <dict or list> data which stored
    :param dumper: <class> dump provider
    :return: None
    """
    as_json = json_dumps(data, indent=4, sort_keys=True, cls=dumper)
    with open(filename, "wt") as fh:
        fh.write(as_json)
    #_logger.debug("JSON DUMP. FILE: '{}'".format(filename))


def json_read(filename, reader=ExtendedJSONDecoder, *args, **kwargs):
    """
    Load data from JSON file
    :param filename: JSON Filename
    :param args: params will be passed to low level json parser
    :param kwargs: params will be passed to low level json parser
    :return: <dict or list>
    """
    loader = kwargs.pop('cls', reader)
    with open(filename, "rb") as fh:
        data_as_string = fh.read()
        if isinstance(data_as_string, bytes):
            data_as_string = data_as_string.decode(encoding='utf-8')
        # _logger.debug("JSON LOAD. FILE: '{}'".format(filename))
        return json.loads(data_as_string, *args, cls=loader,  **kwargs)


# todo - remove this method
def json_file_write(filename, data, dumper=ExtendedJsonEncoder):
    return json_write(filename, data, dumper)
    # as_json = json_dumps(data, indent=4, sort_keys=True, cls=dumper)
    # with open(filename, "wt") as fh:
    #     fh.write(as_json)


def as_json(funct):
    @wraps
    def wrapper(obj, *args, **kwargs):
        return to_json(funct(obj, **kwargs))
    return wrapper


def to_json(obj=None, **kwargs):
    obj = obj if obj is not None else dict()
    return json_dumps(obj, indent=kwargs.pop('indent', 2))

