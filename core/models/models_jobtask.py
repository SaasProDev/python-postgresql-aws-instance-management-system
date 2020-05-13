import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

from .base_models import CreatedUpdatedModel
from .constants import ORGANISATION_MODEL


class RunnerTask(CreatedUpdatedModel):
    """
    Runner Task
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    obj = models.CharField(max_length=100, blank=False, null=False)
    obj_id = models.IntegerField(default=0, blank=False)
    state = models.CharField(max_length=100, blank=False, null=False, default='New')
    ident = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        ordering = ['obj', 'obj_id', 'state']
        unique_together = ['obj', 'obj_id', 'state', 'ident']

    def __str__(self):
        return str(self.uuid)


class Job(CreatedUpdatedModel):
    name        = models.CharField(max_length=100, blank=True)
    ident       = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status      = models.CharField(max_length=100, blank=True)
    rc          = models.CharField(max_length=100, blank=True)
    stats       = JSONField(blank=True, default=dict, editable=True, null=True)
    logs        = JSONField(blank=True, default=dict, editable=True, null=True)
    artifacts   = JSONField(blank=True, default=dict, editable=True, null=True)

    stdout      = models.TextField(null=True, blank=True)

    inventory   = JSONField(blank=True, default=dict, editable=True, null=True)
    command     = JSONField(blank=True, default=dict, editable=True, null=True)
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    private_data_dir = models.CharField(max_length=100, blank=True)
    namespace   = models.CharField(max_length=100, blank=True)
    kind        = models.CharField(max_length=200, blank=True, default='job')

    start_time  = models.DateField(auto_now_add=True, blank=True, null=True)
    finish_time = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['ident', ]
        unique_together = ['ident', 'name', 'organization']

    def __str__(self):
        return str(self.ident)
