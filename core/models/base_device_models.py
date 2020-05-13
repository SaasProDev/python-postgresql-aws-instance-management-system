import uuid
import traceback
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from logging import getLogger

from .base_models import CreatedUpdatedModel


from .constants import CLOUD_LISTS, ORGANISATION_MODEL
from .constants import DEFAULT_CREDENTIAL_SCHEMA, ACTION_CHOICES

from .models_project import Project

_logger = getLogger(__name__)

STATUS_CHOICES = settings.STATUS_CHOICES


# todo compare against JobTemplate
class DeviceTemplate(CreatedUpdatedModel):
    """
    Template for all devices (physical and virtual)
    """
    class Meta:
        abstract = True

    name        = models.CharField(max_length=100, blank=True)
    label       = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True)
    fqdn        = models.CharField(max_length=200, blank=True)
    model       = models.CharField(max_length=200, blank=True)
    kind        = models.CharField(max_length=200, default='generic')
    uuid        = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    sn          = models.CharField(max_length=200, blank=True, verbose_name=_('Serial Number'),
                          help_text=_("Specifies the serial number of the device if exist"))

    # organization= models.ForeignKey(ORGANISATION_MODEL, related_name='%(class)ss',
    #                                  on_delete=models.PROTECT, blank=True, null=True)

    project      = models.ForeignKey(Project, related_name='%(class)ss', on_delete=models.DO_NOTHING, blank=True, null=True)

    credentials = JSONField(blank=True, default=dict, editable=True, null=True)
    inputs      = JSONField(blank=True, default=dict, editable=True, null=True)
    schema      = JSONField(blank=True, default=dict, editable=True, null=True)

    cloud       = models.BooleanField(verbose_name=_("cloud based"), default=False)

    primary_ip  = models.GenericIPAddressField(null=True, blank=True)
    primary_ip6 = models.GenericIPAddressField(null=True, blank=True)

    # todo max_length=20 will be enough  - Mac example: '00:26:57:00:1f:02'
    primary_mac = models.CharField(max_length=200, blank=True)
    primary_domain = models.CharField(max_length=200, blank=True)

    status      = models.CharField(max_length=200, blank=True, choices=STATUS_CHOICES, default='running')
    action      = models.CharField(max_length=200, blank=True, choices=ACTION_CHOICES, default='start')
    facts       = JSONField(blank=True, default=dict, editable=True, null=True)
    setfacts    = JSONField(blank=True, default=dict, editable=True, null=True)
    applications = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    # todo what this?
    ident       = models.CharField(max_length=200, blank=True)

    definition = JSONField(blank=True, default=dict, editable=True, null=True)

    unique_keys = HStoreField(blank=True, default=dict, null=True, verbose_name=_("unique keys"),
                              help_text=_("Unique key(s) for ansible callback"))

    hosted      = models.CharField(max_length=200, null=True , blank=True)

    # todo move ALL FIELDS BELOW into a single JSON field
    processors  = JSONField(blank=True, default=dict, editable=True, null=True)
    disks       = JSONField(blank=True, default=dict, editable=True, null=True)
    lvm         = JSONField(blank=True, default=dict, editable=True, null=True)
    lsblk       = JSONField(blank=True, default=dict, editable=True, null=True)
    mounts      = JSONField(blank=True, default=dict, editable=True, null=True)
    memory      = JSONField(blank=True, default=dict, editable=True, null=True)
    ipaddresses = JSONField(blank=True, default=dict, editable=True, null=True)
    ipv4        = JSONField(blank=True, default=dict, editable=True, null=True)
    ipv6        = JSONField(blank=True, default=dict, editable=True, null=True)
    interfaces  = JSONField(blank=True, default=dict, editable=True, null=True)
    svc         = JSONField(blank=True, default=dict, editable=True, null=True)
    containers  = JSONField(blank=True, default=dict, editable=True, null=True)
    hardware    = JSONField(blank=True, default=dict, editable=True, null=True)
    os          = JSONField(blank=True, default=dict, editable=True, null=True)
    runner      = JSONField(blank=True, default=dict, editable=True, null=True)

    tags = models.ManyToManyField('Tag', verbose_name=_("tags"), blank=True, help_text=_("Select tag(s)"))


    def save(self, *args, **kwargs):
        if self.kind:
            if self.kind in CLOUD_LISTS:
                self.cloud = True
            if not self.schema:
                self.schema = DEFAULT_CREDENTIAL_SCHEMA
        super().save(*args, **kwargs)


#todo remove Duplicate for JobBased
    def live_time(self, since=None):
        from sysutils.utils.timeutils import sting_to_date, date_time_now, display_time
        now = date_time_now()
        seconds = (now - self.created).total_seconds()
        hours = round(seconds / (60 * 60), 2)

        return {'seconds': seconds,
                'hours': hours,
                'human': display_time(seconds)
                }
