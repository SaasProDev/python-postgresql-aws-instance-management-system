import uuid

from django.db import transaction
from django.contrib.auth.models import AbstractUser
from rest_framework.reverse import reverse
from django.conf import settings
from logging import getLogger
from .permission_checker import check_permission_to_object, restricted_ids, get_quireyset

AUTH_USER_MODEL = 'account.User'
from .models_common import *
from .models_permission import UserObjectRole, GroupObjectRole
from .models_permission import FULL_ACCESS_PERMISSION, READ_ONLY_PERMISSION

from core.frontend_helper import organization_from_form


_logger = getLogger(__name__)


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    teams           = models.ManyToManyField('Team', through='Teams', related_name='user_set')
    organizations   = models.ManyToManyField('Organization', through='UserOrganizations', related_name='organization_set')

    owner = models.ForeignKey('self', related_name='subsidiaries', on_delete=models.PROTECT, blank=True, null=True)

    objects = ExtendedUserManager()

    @property
    def is_system_administrator(self):
        return self.is_active and self.is_authenticated and self.is_staff and self.is_superuser

    @property
    def is_system_auditor(self):
        return self.is_active and self.is_authenticated and self.is_staff

    def has_perms(self, perms, obj=None):
        return check_permission_to_object(self, perms, obj)

    def ids_permissions_for(self, model):
        return restricted_ids(self, model)

    def list_queryset_for(self, model, mode='read'):
        if self.is_system_auditor or self.is_system_administrator:
            return model.objects.all()
        return get_quireyset(self, model, mode)

    def get_default_organization(self):
        _logger.warning("*** DEFAULT ORGANISATION - PLEASE FIX! ***")
        #own_organizations
        return self.organizations.first() \
               or Organization.objects.filter(name=settings.DEFAULT_ORGANISATION_NAME).first()

    def post_create(self, user_creator, *args, **kwargs):
        from core.models.models_project import Project
        self.owner = user_creator
        self.is_active = True
        self.is_staff = False
        form_data = kwargs.get('form_data')
        self.set_password(form_data['password'])

        organization = organization_from_form(user_creator, *args, **kwargs)
        role = form_data['organization_role']
        UserOrganizations.objects.create(organization=organization, user=self, role=role)

        group_name = "Full Access" if role in ['admin', ] else "Read Access"
        access_group = AccessGroup.objects.filter(name=group_name, organization=organization).first()
        AccessGroups.objects.create(user=self, access_group=access_group)
        _logger.info("User '{}' added to group '{}' for organisation: '{}'".format(self, group_name, organization))

        if role in ['admin', 'user']:
            project_name = "{} Default Project".format(self.username)
            project_description = "Auto created"
            Project.create(organization, self, name=project_name, description=project_description)
            _logger.debug("Default Project for '{}' created.".format(self))
        else:
            _logger.debug("No Default Project for user '{}' role='{}'".format(self, role))

        # UserObjectRole.objects.create(self, organization, FULL_ACCESS_PERMISSION, organization)

    def get_available_objects(self, model, mode='read'):
        if self.is_system_administrator or (mode == 'read' and self.is_system_auditor):
            return model.objects.all()
        return get_quireyset(self, model, mode)

    def check_is_available_object(self, obj, mode='read'):
        # todo Implement
        _logger.warning("*** This method not implemented yet... returns default value. ***")
        return True



class AccessGroup(BaseModel):
    NAME_SIZE = 100
    DESCRIPTION_SIZE = 1024
    name = models.CharField(max_length=NAME_SIZE, blank=False, null=False)
    description = models.CharField(max_length=DESCRIPTION_SIZE, blank=True, null=True)
    organization = models.ForeignKey('Organization', related_name='access_group_set', on_delete=models.DO_NOTHING, null=True)

    objects = BaseModelManager()

    class Meta:
        unique_together = ('name', 'organization',)

    def __str__(self):
        return self.name


class AccessGroups(models.Model):
    access_group = models.ForeignKey(AccessGroup, on_delete=models.DO_NOTHING, related_name='user_set')
    user         = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='access_group_set')

    class Meta:
        unique_together = ('user', 'access_group',)


class Team(BaseModel):
    NAME_SIZE = 100
    DESCRIPTION_SIZE = 1024
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=NAME_SIZE, blank=False, null=False)
    description = models.CharField(max_length=DESCRIPTION_SIZE, blank=True, null=True)
    organization = models.ForeignKey('Organization', related_name='team_set', on_delete=models.DO_NOTHING, null=True)

    objects = BaseModelManager()

    class Meta:
        unique_together = ('name', 'organization',)

    def __str__(self):
        return self.name


class Teams(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='teams')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='users')

    class Meta:
        unique_together = ('team', 'user',)


class Organization(BaseModel):
    NAME_SIZE = 100
    DESCRIPTION_SIZE = 1024
    PHONE_SIZE = 32
    KIND_SIZE = 32
    CHOICE_SIZE = 20

    STATUS_CHOICES = settings.STATUS_CHOICES

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="own_organizations", null=True, on_delete=models.DO_NOTHING)

    uuid        = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=NAME_SIZE, unique=True, null=False, blank=False)
    description = models.CharField(max_length=DESCRIPTION_SIZE, blank=True, null=True)
    location    = models.CharField(max_length=100, null=True, blank=True)
    contact     = models.CharField(max_length=100, null=True, blank=True)
    phone       = models.CharField(max_length=PHONE_SIZE, null=True, blank=True)
    email       = models.EmailField(null=True, blank=True)
    info        = models.TextField(blank=True, null=True)
    status      = models.CharField(max_length=CHOICE_SIZE, blank=True, choices=STATUS_CHOICES, default='running')
    kind        = models.CharField(max_length=KIND_SIZE, blank=True, default='organization')

    headquarter = models.ForeignKey('self', related_name='subsidiaries', on_delete=models.PROTECT, blank=True, null=True)

    objects = BaseModelManager()

    class Meta:
        ordering = ['name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name

    def get_absolute_url(self, request=None):
        return reverse('organization-detail', args=[str(self.id)], request=request)

    def compose_permission_staff(self, user):
        from account.models import IMPORTANT_MODELS as IMPORTANT_ACCOUNT_MODELS
        from core.models import IMPORTANT_MODELS as IMPORTANT_CORE_MODELS

        full_access = AccessGroup.objects.create(name="Full Access", organization=self)
        read_access = AccessGroup.objects.create(name="Read Access", organization=self)

        AccessGroups.objects.create(user=user, access_group=full_access)

        for model in IMPORTANT_ACCOUNT_MODELS + IMPORTANT_CORE_MODELS:
            GroupObjectRole.objects.create(full_access, self, FULL_ACCESS_PERMISSION, model)
            GroupObjectRole.objects.create(read_access, self, READ_ONLY_PERMISSION, model)

    def post_create(self, user, *args, **kwargs):
        self.owner = user
        UserOrganizations.objects.create(organization=self, user=user, role=UserOrganizations.ROLE_OWNER)
        self.compose_permission_staff(user)


class UserOrganizations(models.Model):
    ROLES = (
        ("user", "user"),
        ("owner", "owner"),
        ("admin", "admin"),
        ("auditor", "auditor"),
        ("reporter", "reporter"),
        ("visitor", "visitor"),
    )

    ROLE_OWNER = "owner"
    ROLE_DEFAULT = "visitor"

    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    user         = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    role         = models.CharField(max_length=12, choices=ROLES, default=ROLE_DEFAULT)

    class Meta:
        unique_together = ('user', 'organization',)

#
# def attach_user_to_organisation(user, organisation, role):
#     organisation = Organization.objects.get(pk=organisation_id)
#     UserOrganizations.objects.create(organization=organisation, user=user, role=role)
