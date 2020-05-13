# Python
import json
import yaml
import logging
import os
import re
import subprocess
import stat
import urllib.parse
import threading
import contextlib
import tempfile
import psutil
import paramiko
import logging

from functools import reduce, wraps


from decimal import Decimal

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignObjectRel, ManyToManyField
from django.db.models.query import QuerySet
from django.db.models import Q

# Django REST Framework
from rest_framework.exceptions import ParseError
from django.utils.encoding import smart_str
from django.utils.text import slugify
from django.apps import apps



from django.db.models import ForeignKey


_logger = logging.getLogger(__name__)

def workflow_engine(model, fieldname):
    '''returns None if not foreignkey, otherswise the relevant model'''
    field_object, model, direct, m2m = model._meta.get_field_by_name(fieldname)
    if not m2m and direct and isinstance(field_object, ForeignKey):
        return field_object.rel.to
    return None
    # _logger.debug("Exception: {}".format(ex))