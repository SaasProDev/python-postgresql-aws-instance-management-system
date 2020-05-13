import logging
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from django.contrib.auth import get_user_model

from .base_viewset import DefaultBaseViewSet, DefaultPermittedBaseViewSet
from .models import (Organization, User, Team, AccessGroup, GroupObjectRole, UserObjectRole)
from .models import (Group, Permission)

from .pagination import DefaultPagination
from .serializer import (
    OrganizationSerializer,
    UserSerializer,
    UserUpdateCreateSerializer,
    UserPermisionsInfoSerializer,
    TeamSerializer,
    AccessGroupSerializer,
    AccessPermissionGroupSerializer,
    AccessPermissionUserSerializer,
    GroupSerializer,
    PermissionSerializer
)

from .permissions import DefaultRoleBasedPermissions

_logger = logging.getLogger(__name__)


class OrganizationViewSet(DefaultPermittedBaseViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    filter_backends  = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields    = ('name', 'description', 'location', 'contact', 'phone', 'email', 'info',)
    filterset_fields = ('id', 'name',)
    ordering_fields  = ('name',)


class UserViewSet(DefaultPermittedBaseViewSet):
    serializer_class = UserSerializer
    serializer_class_create = UserUpdateCreateSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = get_user_model().objects.all().order_by('-date_joined')
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        elif self.action in ('create', 'update', 'partial_update'):
            return self.serializer_class_create
        else:
            raise Exception("Cannot perform User's action: '{}'".format(self.action))

    def perform_update(self, serializer):
        serializer.perform_update()


class TeamViewSet(DefaultPermittedBaseViewSet):
    serializer_class = TeamSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Team.objects.all()


class GroupViewSet(DefaultPermittedBaseViewSet):
    serializer_class = GroupSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = Group.objects.all().order_by('name')
        return queryset

# todo NOT USED - remove
class PermissionViewSet(DefaultPermittedBaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = DefaultPagination


class AccessGroupViewSet(DefaultPermittedBaseViewSet):
    serializer_class = AccessGroupSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = AccessGroup.objects.all().order_by('name')
        return queryset


class AccessGroupRulesViewSet(DefaultPermittedBaseViewSet):
    queryset = GroupObjectRole.objects.all()
    serializer_class = AccessPermissionGroupSerializer
    pagination_class = DefaultPagination


class AccessUserRulesViewSet(DefaultPermittedBaseViewSet):
    queryset = UserObjectRole.objects.all()
    serializer_class = AccessPermissionUserSerializer
    pagination_class = DefaultPagination


class UserPermisionsInfoViewSet(DefaultBaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserPermisionsInfoSerializer
    pagination_class = DefaultPagination
