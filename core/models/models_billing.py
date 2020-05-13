from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.conf import settings


class ResourceAliveHistory(models.Model):
    MAX_TASK_NAME_LENGTH = 16
    # RESOURCE_STATUS_CHOICES = (
    #     ('up', 'up'),
    #     ('down', 'down'),
    # )
    model = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    resource_id = models.PositiveIntegerField(db_index=True)
    # resource_status = models.CharField(max_length=6, choices=RESOURCE_STATUS_CHOICES)
    resource_status = models.CharField(max_length=16)

    task_id = models.UUIDField(null=True)
    task_mode = models.CharField(max_length=MAX_TASK_NAME_LENGTH)

    task_initialised = models.DateTimeField(auto_now_add=True)
    task_completed   = models.DateTimeField(null=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return "{}.{}:{}".format(self.model.app_label, self.model.model, self.resource_id)

    @staticmethod
    def get_content_type(model):
        model = apps.get_model(model) if isinstance(model, str) else model
        return ContentType.objects.get_for_model(model) if model else None


