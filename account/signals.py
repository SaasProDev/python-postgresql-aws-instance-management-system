from django.dispatch import receiver
from django.db.models import signals

from logging import getLogger
from .models import User, Team

_logger = getLogger(__name__)


@receiver(signals.post_save, sender=User, dispatch_uid="update_user")
def update_user(sender, instance, created, update_fields, *args, **kwargs):
    _logger.info("User: '{}' CREATED / UPDATED".format(instance))

