import uuid
import logging
import pprint
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .base_models import CreatedUpdatedModel

from .constants import CLOUD_LISTS, ORGANISATION_MODEL
from .constants import DEFAULT_CREDENTIAL_SCHEMA, ACTION_CHOICES

from .models_project import Project

_logger = logging.getLogger(__name__)

STATUS_CHOICES = settings.STATUS_CHOICES

# INFRASTRUCTURE_MODEL = 'Infrastructure'
INFRASTRUCTURE_MODEL = 'IaaS'


class JobEvent(CreatedUpdatedModel):
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False)
    counter     = models.IntegerField(default=0, blank=True)
    stdout      = models.TextField(blank=True)
    start_line  = models.IntegerField(default=0, blank=True)
    end_line    = models.IntegerField(default=0, blank=True)
    runner_ident= models.CharField(max_length=100, blank=True)
    event       = models.CharField(max_length=100, blank=True)
    pid         = models.IntegerField(default=0, null=True, blank=True)
    parent_uuid = models.CharField(max_length=100, blank=True)
    event_data  = JSONField(blank=True, default=dict, editable=True, null=True)
    job         = models.ForeignKey('Job', related_name='%(class)ss',
                                    on_delete=models.PROTECT, blank=True, null=True)
    namespace   = models.CharField(max_length=100, blank=True)
    kind        = models.CharField(max_length=200, blank=True, default='job_event')

    # created_time = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['uuid', 'counter', 'event']

    def __str__(self):
        return str(self.uuid)


class AhomeJobTemplate(CreatedUpdatedModel):
    """
    Template for all ahome Job related modules
    """
    class Meta:
        abstract = True

    name         = models.CharField(max_length=100, blank=True)
    label        = models.CharField(max_length=200, blank=True)
    description  = models.CharField(max_length=200, blank=True, null=True)
    action       = models.CharField(max_length=200, blank=True, choices=ACTION_CHOICES, default='start')
    ahomefile    = JSONField(blank=True, default=dict, editable=True, null=True)
    project      = models.ForeignKey(Project, related_name='%(class)ss', on_delete=models.DO_NOTHING, blank=True, null=True)
    #organization = models.ForeignKey(ORGANISATION_MODEL, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    #infrastructure= models.ForeignKey(INFRASTRUCTURE_MODEL, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    iaas         = models.ForeignKey(INFRASTRUCTURE_MODEL, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    target       = models.CharField(max_length=200, blank=True)
    kind         = models.CharField(max_length=200, default='generic')
    hosted       = models.CharField(max_length=200, blank=True)
    opts         = JSONField(blank=True, default=dict, editable=True, null=True)
    status       = models.CharField(max_length=200, blank=True, choices=STATUS_CHOICES, default='running')
    output       = models.CharField(max_length=200, blank=True)
    ident        = models.CharField(max_length=200, blank=True)
    uuid         = models.UUIDField(default=uuid.uuid4, editable=False)
    cloud        = models.BooleanField(verbose_name=_("cloud based"), default=False)
    unique_keys  = HStoreField(blank=True, default=dict, null=True,
                              verbose_name=_("unique keys"), help_text=_("Unique key(s) for ansible callback"))
    source       = JSONField(blank=True, default=dict, editable=True, null=True)
    # todo Encript this field
    credentials  = JSONField(blank=True, default=dict, editable=True, null=True)
    definition   = JSONField(blank=True, default=dict, editable=True, null=True)
    facts        = JSONField(blank=True, default=dict, editable=True, null=True)
    setfacts     = JSONField(blank=True, default=dict, editable=True, null=True)
    inputs       = JSONField(blank=True, default=dict, editable=True, null=True)
    applications = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    schema       = JSONField(blank=True, default=dict, editable=True, null=True)
    runner       = JSONField(blank=True, default=dict, editable=True, null=True)
    tags         = models.ManyToManyField('Tag', verbose_name=_("tags"), blank=True, help_text=_("Select tag(s)"))
    # tags = ArrayField(models.CharField(max_length=200), blank=True)

    def save(self, *args, **kwargs):
        if self.kind:
            if self.kind in CLOUD_LISTS:
                self.cloud = True
            if not self.schema:
                self.schema = DEFAULT_CREDENTIAL_SCHEMA
        if not self.unique_keys:
            self.unique_keys = dict(uuid=self.uuid)

        return super().save(*args, **kwargs)

    def live_time(self, since=None):
        from sysutils.utils.timeutils import sting_to_date, date_time_now, display_time
        now = date_time_now()
        seconds = (now - self.created).total_seconds()
        hours = round(seconds / (60 * 60), 2)

        return {
            'seconds': seconds,
            'hours': hours,
            'human': display_time(seconds)
            }

    # def pre_create(self, user, *args, **kwargs):
    #     try:
    #        # self.owner = user
    #       form_data = kwargs.get('form_data')
    #       _logger.debug("PRE_CREATE - FORM DATA \n{}".format(pprint.pformat(form_data, indent=4)))
    #     except:
    #         pass
    #     pass