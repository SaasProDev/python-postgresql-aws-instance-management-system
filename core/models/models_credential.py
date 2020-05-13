import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ..utils.common import generate_inputs_sshkeys
from .base_models import CreatedUpdatedModel
from .constants import CLOUD_LISTS, ORGANISATION_MODEL


STATUS_CHOICES = settings.STATUS_CHOICES


class Credential(CreatedUpdatedModel):
    """
    Credential
    """
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind        = models.CharField(max_length=200, default='generic')
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='credentials', on_delete=models.PROTECT, blank=True, null=True)
    inputs      = JSONField(blank=True, default=dict, editable=True, null=True)
    cloud       = models.BooleanField(verbose_name=_("cloud credential"), default=False)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'Credential'
        verbose_name_plural = 'Credentials'

    def __str__(self):
        return self.name

# todo What the DIFFERENCE 'UserSecret' vs 'UserKey' ??


class UserSecret(CreatedUpdatedModel):
    """
    User Secret
    """
    USER_SSHKEY  = 'sshkey'
    USER_SECRET  = 'secret'
    USER_CUSTOM  = 'custom'
    USER_STATUS  = [
           (USER_SSHKEY, _('SSH Key')),
           (USER_SECRET, _('Username and Password')),
           (USER_CUSTOM, _('Custom authentication')),
       ]
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind        = models.CharField(max_length=200, choices=USER_STATUS, default=USER_SSHKEY)
    fingerprint = models.CharField(max_length=250, blank=True)
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='usersecrets',
                                     on_delete=models.PROTECT, blank=True, null=True)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False)
    schema      = JSONField(blank=True, default=dict, editable=True, null=True)
    injector    = JSONField(blank=True, default=dict, editable=True, null=True)
    inputs      = JSONField(blank=True, default=dict, editable=True, null=True)
    cloud       = models.BooleanField(verbose_name=_("cloud key"), default=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'User Secret'
        verbose_name_plural = 'User Secrets'


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.inputs:
            self.inputs = generate_inputs_sshkeys(self.inputs)
        super(UserSecret, self).save(*args, **kwargs)


class UserKey(CreatedUpdatedModel):
    """
    User Keys
    """
    USER_SSHKEY  = 'sshkey'
    USER_SECRET  = 'secret'
    USER_CUSTOM  = 'custom'
    USER_STATUS  = [
           (USER_SSHKEY, _('SSH Key')),
           (USER_SECRET, _('Username and Password')),
           (USER_CUSTOM, _('Custom authentication')),
       ]
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    kind        = models.CharField(max_length=200, choices=USER_STATUS, default=USER_SSHKEY)
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='userkeys',
                                     on_delete=models.PROTECT, blank=True, null=True)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False)
    schema      = JSONField(blank=True, default=dict, editable=True, null=True)
    injector    = JSONField(blank=True, default=dict, editable=True, null=True)

    inputs      = JSONField(blank=True, default=dict, editable=True, null=True)
    cloud       = models.BooleanField(verbose_name=_("cloud key"), default=False)

    keykind     = models.CharField(max_length=200, default='rsa')
    keysize     = models.IntegerField(default=2048)
    fingerprint = models.CharField(max_length=250, blank=True)
    publickey   = models.TextField(blank=True, null=True)

    # todo Encrypt these field
    privatekey  = models.TextField(blank=True, null=True)
    passphrase  = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'User Key'
        verbose_name_plural = 'User Keys'

    def __str__(self):
        return self.name
