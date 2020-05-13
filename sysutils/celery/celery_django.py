"""
Celery app initialisation
"""

from attrdict import AttrDict
from .celery_extender import CeleryExtender
from django.conf import settings

from logging import getLogger
_logger = getLogger(__name__)


def celery_connections():
    result = {}
    try:
        for name, params in settings.CELERY.items():
            result[name] = AttrDict({name: params.get(name) for name in params.keys()})
    except:
        _logger.warning("No CELERY extra connector. SKIPPED")
    return result


connectors = celery_connections()
celery_appdjango = CeleryExtender(__name__, celery_connections())

urls = ",".join([x.BROKER_URL for x in connectors.values()])
_logger.info("***** Django CELERY CONNECTED."
                         " NUMBER OF CHANNELS: [{}];"
                         " BROKER_URLS: {} ******".format(len(connectors), urls))

