import os
import django
from django.conf import settings


try:
    already_inited = hasattr(settings, 'FRAMEWORK') and settings.FRAMEWORK == "DJANGO"
except:
    already_inited = False
if not already_inited:
    mode = os.environ.get('ENVIRONMENT_MODE', 'develop').lower()
    settings_file_name = "ahome.settings"
    print("*** Django settings: '{}' ***".format(settings_file_name))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file_name)
    django.setup()

setattr(settings, "APPLICATION_TYPE", "CELERY_WORKER")
os.environ['APPLICATION_TYPE'] = "CELERY_WORKER"

from .celery_django import celery_appdjango
