from django.http import Http404
from rest_framework.permissions import BasePermission, DjangoObjectPermissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from pprint import pprint


def check_as_system_wide(request):
    user = request.user
    if not user or user.is_anonymous:
        return False
    if user.is_system_administrator:
        return True
    if user.is_system_auditor and DefaultRoleBasedPermissions.is_safe_method(request):
        return True
    return False


class DefaultRoleBasedPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET':      ['%(app_label)s.%(model_name)s:read'],
        'OPTIONS':  ['%(app_label)s.%(model_name)s:read'],
        'HEAD':     ['%(app_label)s.%(model_name)s:read'],
        'POST':     ['%(app_label)s.%(model_name)s:add'],
        'PUT':      ['%(app_label)s.%(model_name)s:edit'],
        'PATCH':    ['%(app_label)s.%(model_name)s:edit'],
        'DELETE':   ['%(app_label)s.%(model_name)s:delete'],
    }

    @classmethod
    def is_safe_method(cls, request):
        return request.method in SAFE_METHODS

    @staticmethod
    def get_user(request):
        return request.user \
            if request.user \
               and not request.user.is_anonymous \
               and request.user.is_authenticated \
            else None

    def has_permission(self, request, view):
        return check_as_system_wide(request) \
                or self._has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        return check_as_system_wide(request) \
               or self._has_object_permission(request, view, obj)

    def _has_object_permission(self, request, view, obj):
        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user

        perms = self.get_required_object_permissions(request.method, model_cls)

        if not user.has_perms(perms, obj):
            if request.method in SAFE_METHODS:
                raise Http404

            read_perms = self.get_required_object_permissions('GET', model_cls)
            if not user.has_perms(read_perms, obj):
                raise Http404
            return False
        return True



class StaffOnlyPermissions(DefaultRoleBasedPermissions):
    def has_permission(self, request, view):
        return check_as_system_wide(request)

    def has_object_permission(self, request, view, obj):
        return check_as_system_wide(request)
