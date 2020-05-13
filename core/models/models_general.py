from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from .base_models import CreatedUpdatedModel
from .constants import ORGANISATION_MODEL


STATUS_CHOICES = settings.STATUS_CHOICES


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    font_awesome = models.CharField(max_length=60, blank=False)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Container(CreatedUpdatedModel):
    """
    Containers and Pods
    """
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    hosted = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='containers', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['name',]


class WizardBox(CreatedUpdatedModel):
    """
    Credential
    """
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind        = models.CharField(max_length=200, default='generic')
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='wizardboxes',
                                     on_delete=models.PROTECT, blank=True, null=True)
    schema = JSONField(blank=True, default=dict, editable=True, null=True)
    inputs = JSONField(blank=True, default=dict, editable=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'WizardBox'
        verbose_name_plural = 'WizardBoxes'


    def __str__(self):
        return self.name
