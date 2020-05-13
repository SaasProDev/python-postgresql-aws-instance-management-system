from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from .base_device_models import DeviceTemplate
from .models_job_based import Provider, IaaS

STATUS_CHOICES = settings.STATUS_CHOICES


class Device(DeviceTemplate):
    """
    BareMetal / Hypervisors /  Appliances / Storage Unit
    """

    provider        = models.ForeignKey(Provider, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    virtualmachines = JSONField(blank=True, default=dict, editable=True, null=True)
    sdn             = JSONField(blank=True, default=dict, editable=True, null=True)
    prefixes        = JSONField(blank=True, default=dict, editable=True, null=True)

    class Meta:
        ordering = ['name' ,]

    def __str__(self):
        return str(self.name)
