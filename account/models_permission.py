import uuid
from functools import reduce
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from core.utils.lazy_property import lazy_property

from .utils import get_selector, get_content_type

from logging import getLogger

AUTH_USER_MODEL = 'account.User'

from .models_common import *


_logger = getLogger(__name__)


class ObjectRoleManager(models.Manager):
    ROLE_KIND = None

    def default_name(self, severity, permissions):
        return "FULL" if severity == self.model.full_access_severity() \
                else ".".join(permissions)

    def is_instance(self, obj_or_model):
        return isinstance(obj_or_model, models.Model)

    def role_kind(cls):
        return cls.ROLE_KIND

    def created_ext(self, **params):
        role = self.model(**params)
        role.save(using=self._db)
        return role

    def create(self, user_or_group, organization, permissions=None, obj_or_model=None, name=None):
        severity = self.model.compose_role(permissions) if permissions else self.model.ANY_ACCESS_PERMISSION
        name = name or self.default_name(severity, permissions)
        selector = get_selector(obj_or_model, "ALL", "MODELS")
        ctype = get_content_type(obj_or_model) if obj_or_model else None

        params = {
            'severity':  severity,
            self.role_kind(): user_or_group,
            'name': "{}:{}".format(selector, name),
            'organization': organization
        }
        if organization:
            params['organization'] = organization

        if ctype:
           params.update({
                'natural_key': "{}".format(selector),
                'ctype': ctype
           })

        if obj_or_model and self.is_instance(obj_or_model):
            params['obj_id'] = obj_or_model.id

        role = self.model(**params)
        role.save(using=self._db)
        return role


class ObjectGroupRoleManager(ObjectRoleManager):
    ROLE_KIND = 'group'


class ObjectUserRoleManager(ObjectRoleManager):
    ROLE_KIND = 'user'


class BaseObjectRole(BaseModel):
    ACTIONS = {
        'read':     1,
        'add':      1 << 1,
        'edit':     1 << 2,
        'delete':   1 << 3,
        'execute':  1 << 4,
        'grant':    1 << 5,
    }

    ANY_ACCESS_PERMISSION = 0

    NAME_SIZE = 160
    NATURAL_KEY_SIZE  = 100
    obj_id      = models.PositiveIntegerField(unique=False, blank=True, null=True, editable=True)
    obj_ids     = models.TextField(default="")
    ctype       = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    severity    = models.IntegerField(unique=False, default=ANY_ACCESS_PERMISSION)
    natural_key = models.CharField(max_length=NATURAL_KEY_SIZE, blank=True, null=True)
    name        = models.CharField(max_length=NAME_SIZE, blank=True, null=True)
    # obj_ids     = JSONField(blank=True, default=None, editable=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @classmethod
    def full_access_premisisons(cls):
        return cls.ACTIONS.keys()

    @classmethod
    def read_access_premisisons(cls):
        return ['read',  'execute']

    @classmethod
    def compose_role(cls, actions):
        return reduce(lambda value, name: value | cls.ACTIONS[name], actions, 0)

    @classmethod
    def full_access_severity(cls):
        return cls.compose_role(cls.full_access_premisisons())

    @classmethod
    def use_access_premisison(cls):
        return cls.compose_role(cls.read_access_premisisons())

    def unpack_objids(self, ids):
        include = []
        exclude = []

        for id in ids:
            if id > 0:
                include.append(id)
            else:
                exclude.append(-id)
        return {
            '+': set(include),
            '-': set(exclude)
        }

    @property
    def objids(self):
        from json import loads
        result = {}
        for key, value in self.ACTIONS.items():
            if value & self.severity:
                if len(self.obj_ids):
                    result[key] = self.unpack_objids(loads(self.obj_ids))
                else:
                    result[key] = self.unpack_objids([])
                    result[key]['*'] = True
        return result

    def check_objid(self, id, mode):
        if not self.objids.get(mode):
            return False
        idds = self.objids[mode]
        return id in idds['+'] if idds['+'] else id not in idds['-']


class UserObjectRole(BaseObjectRole):
    organization = models.ForeignKey('Organization', related_name='user_roles_set', on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='roles_set', on_delete=models.DO_NOTHING)

    objects = ObjectUserRoleManager()


class GroupObjectRole(BaseObjectRole):
    organization = models.ForeignKey('Organization', related_name='group_roles_set', on_delete=models.DO_NOTHING, null=False)
    group = models.ForeignKey('AccessGroup', related_name='roles_set', on_delete=models.DO_NOTHING)

    objects = ObjectGroupRoleManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.group.organization != self.organization:
            raise Exception("Not consistences GroupObjectRole: [{}:{}]".format(self.group.organization, self.organization))
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)


FULL_ACCESS_PERMISSION  = UserObjectRole.full_access_premisisons()
READ_ONLY_PERMISSION    = UserObjectRole.read_access_premisisons()
