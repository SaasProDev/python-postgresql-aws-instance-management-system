from pprint import pprint
import copy
from logging import getLogger
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Organization, UserOrganizations, Team, Teams, User, AccessGroup, GroupObjectRole, UserObjectRole
from .models import FULL_ACCESS_PERMISSION
from .models import Group, Permission
from ahome.base_serializer import BaseSerializer
from ahome.base_serializer import OrganizationBaseSerializer

import account.models
import core.models

_logger = getLogger(__name__)


def object_by_id(cls, id):
    return cls.objects.get(pk=id)


def get_default_organization():
    return Organization.objects.filter(name=settings.DEFAULT_ORGANISATION_NAME).first()


def add_user_organisation(user, organization):
    UserOrganizations.objects.create(user=user, organization=organization)


def add_user_group_by_id(user, id):
    user.groups.add(object_by_id(Group, id))


def add_user_team_by_id(user, id):
    return Teams.objects.create(user=user, team=object_by_id(Team, id))


def add_user_organization_by_id(user, id):
    return UserOrganizations.objects.create(user=user, organization=object_by_id(Organization, id))


def group_objectrole_by_id(id):
    return GroupObjectRole.objects.get(pk=id)



class ManyToManyFieldSerializer(serializers.Field):
    def __init__(self, source=None, required=False):
        super().__init__(source=source, required=required)

    def to_representation(self, obj):
        return [o.id for o in obj.all()] if obj and hasattr(obj, 'all') else []

    def to_internal_value(self, data):
        return data


class ManyToManyROFieldSerializer(serializers.ReadOnlyField):
    def __init__(self, source=None, required=False):
        super().__init__(source=source, required=required)

    def to_representation(self, obj):
        return [o.id for o in obj.all()] if obj and hasattr(obj, 'all') else []

    def to_internal_value(self, data):
        return data


class DefaultSerializer(serializers.HyperlinkedModelSerializer):
    @transaction.atomic()
    def save(self, **kwargs):
        _logger.debug("Saving {} object..".format(self.Meta.model))
        try:
            return super().save(**kwargs)
        except Exception as ex:
            _logger.debug("Exception: {}".format(ex))
            return None


class TeamSerializer(DefaultSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()
    user_set = ManyToManyFieldSerializer()

    class Meta:
        model = Team
        fields = ('id', 'uuid', 'name', 'organization', 'user_set')


class UserSerializer(DefaultSerializer):
# class UserSerializer(BaseSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()

    organization_set = ManyToManyFieldSerializer('organizations')
    team_set         = ManyToManyFieldSerializer('teams')
    group_set        = ManyToManyFieldSerializer('access_group_set')

    # permissions = serializers.SerializerMethodField('_get_roles')

    class Meta:
        model = User
        fields = ('id', 'uuid', 'username', 'email',
                  'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
                  'team_set', 'organization_set', 'group_set',)


class UserPermisionsInfoSerializer(DefaultSerializer):
    permissions = serializers.SerializerMethodField('_get_roles')

    class Meta:
        model = User
        fields = ('id', 'permissions',)

    def _get_roles(self, obj):
        result = {}
        for model in account.models.IMPORTANT_MODELS + core.models.IMPORTANT_MODELS:
            ctype = ContentType.objects.get_for_model(model)
            app_label, model_name = ctype.natural_key()
            model_perms = []

            for key in FULL_ACCESS_PERMISSION:
                permission = "{}.{}:{}".format(app_label, model_name, key)
                if obj.has_perms([permission]):
                    model_perms.append(key)
            result[model.__name__] = "|".join(model_perms)
            #print("ERR [{}] {}\t\t{}".format(permission, model, ctype.natural_key()))
        return result


class PasswordFieldSerializer(serializers.Field):
    def to_representation(self, obj):
        return "***"

    def to_internal_value(self, data):
        return data



class UserUpdateCreateSerializer(DefaultSerializer):
    password = PasswordFieldSerializer()
    organization_set= ManyToManyFieldSerializer('organizations')
    team_set        = ManyToManyFieldSerializer('teams')
    group_set       = ManyToManyFieldSerializer('groups')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',
                  'team_set', 'organization_set', 'group_set')

    @transaction.atomic()
    def save(self, **kwargs):
        data = copy.deepcopy(self._validated_data)

        routines = {
            "groups": add_user_group_by_id,
            "teams": add_user_team_by_id,
            "organizations": add_user_organization_by_id
        }
        values = {}
        for name in routines.keys():
            values[name] = data.pop(name)

        data['is_staff'] = True
        _logger.warning("*** USER STAFF = TRUE NEED TO BE FIXED!!!! ****")
        # print("USER DATA")
        # pprint(self.data)
        # pprint(data)
        self.instance = User.objects.create_user(**data)

        for name, routine in routines.items():
            ids = values[name] or []
            for id in ids:
                routine(self.instance, id)

        #add_user_organisation(self.instance, get_default_organization())
        _logger.info("User created: {}".format(self.instance))
        return self.instance

    def password_for_update(self):
        password = self._validated_data.pop('password', None)
        return password if password and password != self.data.get('password') else None

    @transaction.atomic()
    def perform_update(self):
        password = self.password_for_update()
        if password:
            self._validated_data['password'] = make_password(password)
        self.update(self.instance, self._validated_data)
        _logger.info("User Updated: {}".format(self.instance))


class GroupSerializer(DefaultSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = ('id', 'name', )


class AccessGroupSerializer(BaseSerializer):
    id = serializers.ReadOnlyField()
    roles_set = ManyToManyROFieldSerializer()

    class Meta:
        model = AccessGroup
        fields = ('id', 'name', 'description', 'organization', 'roles_set')



class AccessPermissionGroupSerializer(DefaultSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = GroupObjectRole
        fields = ('id', 'name', 'natural_key', 'severity', 'obj_ids', 'organization', 'group')

    def create(self, validated_data):
        return self.Meta.model.objects.created_ext(**validated_data)


class AccessPermissionUserSerializer(DefaultSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = UserObjectRole
        fields = ('id', 'name', 'natural_key', 'severity', 'obj_ids', 'organization', 'user')

    def create(self, validated_data):
        return self.Meta.model.objects.created_ext(**validated_data)


class PermissionSerializer(DefaultSerializer):
    id = serializers.ReadOnlyField()
    content_type = serializers.SerializerMethodField("get_content_type")

    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename')

    def get_content_type(self, obj):
        return obj.content_type.id


class OrganizationSerializer(OrganizationBaseSerializer):
    id   = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Organization
        fields = '__all__'
        # fields = ['id', 'name']

    def to_representation(self, instance):
        request = self.context.get('request')

        representation = super().to_representation(instance)
        # representation['admin'] = True

        # representation = super(OrganizationSerializer, self).to_representation(instance)
        if instance.headquarter:
            instance_name = instance.__class__.__name__.lower()

            url = reverse('{}-detail'.format(instance_name), args=[instance.headquarter.id])
            data = dict(
                organization=dict(
                    url=request.build_absolute_uri(url),
                    id=instance.headquarter.id,
                    uuid=instance.headquarter.uuid,
                    name=instance.headquarter.name,
                    kind=instance.headquarter.kind,
                    status=instance.headquarter.status,
                )
            )

            representation.get("summary_fields").update(data)

            representation.update(dict(
                name="{} > {}".format(instance.headquarter.name, instance.name),
                # url2 = instance.get_absolute_url()
            ))
        return representation