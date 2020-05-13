from json import JSONEncoder
from .json_tools import ExtendedJsonEncoder

_default = JSONEncoder.default
JSONEncoder.default = ExtendedJsonEncoder.default
