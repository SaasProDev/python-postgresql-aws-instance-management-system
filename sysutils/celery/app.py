"""
The simplest Celery app initialisation
Copyright tretyak@gmail.com
https://github.com/xmig/celerytasks
"""

import sys
from os import environ

try:
    from uuid import _uuid_generate_random
except:
    """Fix Kombu - because '_uuid_generate_random' was removed """
    import uuid
    uuid._uuid_generate_random = None

sys.path.append("./")

from .appdjango import celery_appdjango
celery_app = celery_appdjango
