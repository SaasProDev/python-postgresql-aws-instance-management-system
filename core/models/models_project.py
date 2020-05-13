import uuid
import logging
from django.db import models
from django.db import IntegrityError, transaction
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from .base_models import CreatedUpdatedModel
from .constants import ORGANISATION_MODEL
from ..frontend_helper import organization_from_form

_logger = logging.getLogger(__name__)

STATUS_CHOICES = settings.STATUS_CHOICES
AUTH_USER_MODEL = settings.AUTH_USER_MODEL


class Project(CreatedUpdatedModel):
    """
    Project - holder for ALL infrastructure items
    """
    KINDS = (
        ("default", "default"),
    )
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    name        = models.CharField(max_length=50)
    public      = models.BooleanField(default=False)
    uuid        = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=200, default="")
    kind        = models.CharField(max_length=12, choices=KINDS, default='default')
    organization= models.ForeignKey(ORGANISATION_MODEL, related_name='projects', on_delete=models.PROTECT, null=False)
    users       = models.ManyToManyField(AUTH_USER_MODEL, through='UserProject', related_name='projects')

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'organization',)

    def __str__(self):
        return self.name

    @classmethod
    @transaction.atomic
    def create(cls, organization, user, **kwargs):
        instance = cls.objects.create(organization=organization, owner=user, **kwargs)
        UserProject.objects.create(project=instance, user=user, role=UserProject.ROLE_OWNER)
        return instance

    def pre_create(self, user, *args, **kwargs):
        self.owner = user
        self.organization = organization_from_form(user, *args, **kwargs)

    def post_create(self, user, *args, **kwargs):
        UserProject.objects.create(project=self, user=user, role=UserProject.ROLE_OWNER)
        _logger.info("Project '{}' successfully created. Owner: '{}'".format(self, user))
        return self


class UserProject(models.Model):
    ROLES = (
        ("user",    "user"),
        ("owner",   "owner"),
        ("admin",   "admin"),
        ("auditor", "auditor"),
        ("reporter","reporter"),
        ("visitor", "visitor"),
    )
    ROLE_OWNER = "owner"
    ROLE_DEFAULT = "visitor"

    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    user    = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    role    = models.CharField(max_length=12, choices=ROLES, default=ROLE_DEFAULT)

    class Meta:
        unique_together = ('user', 'project',)
