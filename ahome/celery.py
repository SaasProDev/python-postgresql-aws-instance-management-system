from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from celery.signals import setup_logging


os.environ['APPLICATION_TYPE'] = "CELERY_WORKER"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahome.settings')


app = Celery('ahome')
app.config_from_object('django.conf:settings', namespace='CELERY')


#
# @setup_logging.connect
# def config_loggers(*args, **kwags):
#     from logging.config import dictConfig
#     from django.conf import settings
#
#     dictConfig(settings.LOGGING)
#
#     setattr(settings, "APPLICATION_TYPE", "CELERY_WORKER")
#     os.environ['APPLICATION_TYPE'] = "CELERY_WORKER"
#
#     # app.log.redirect_stdouts_to_logger(logging.getLogger('CELERY'))

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))