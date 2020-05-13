from django.db import models
from .base_job_models import AhomeJobTemplate
from django.conf import settings

from core.utils import generate_inputs_sshkeys
# from .models_project import Provider

from .constants import ORGANISATION_MODEL

import pprint
from logging import getLogger

_logger = getLogger(__name__)


class Provider(AhomeJobTemplate):
    """
    Provider
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(ORGANISATION_MODEL, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)


class UserCredential(AhomeJobTemplate):
    """
    User Credential
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'User Credential'
        verbose_name_plural = 'User Credentials'

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        return super().save(*args, **kwargs)


# class IaaSManager(models.Manager):
#     def create(self, **data):
#         return super().create(**data)


class IaaS(AhomeJobTemplate):
    """
    Infra as a Service
    """
    # objects = IaaSManager()
    usercredential  = models.ForeignKey(UserCredential, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    userkey         = models.ManyToManyField('UserKey', related_name='%(class)ss', blank=True)
    usersecret      = models.ManyToManyField('UserSecret', related_name='%(class)ss', blank=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        return super().save(*args, **kwargs)


class PaaS(AhomeJobTemplate):
    """
    Platform as a Service
    """
    # provider = models.ForeignKey(Provider, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    usercredential  = models.ForeignKey(UserCredential, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    userkey         = models.ManyToManyField('UserKey', related_name='%(class)ss', blank=True)
    usersecret      = models.ManyToManyField('UserSecret', related_name='%(class)ss', blank=True)
    project         = models.ForeignKey('Project', related_name='%(class)ss', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        super(PaaS, self).save(*args, **kwargs)



class Sdn(AhomeJobTemplate):
    """
    SDN
    """

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Storage(AhomeJobTemplate):
    """
    Storage
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Service(AhomeJobTemplate):
    """
    Service
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Monitoring(AhomeJobTemplate):
    """
    Monitoring
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Security(AhomeJobTemplate):
    """
    Security
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Pki(AhomeJobTemplate):
    """
    PKI
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Backup(AhomeJobTemplate):
    """
    Backup
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Billing(AhomeJobTemplate):
    """
    Billing
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)


class Documentation(AhomeJobTemplate):
    """
    Documentation
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)
