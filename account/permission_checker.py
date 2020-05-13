import uuid
from functools import reduce
from django.conf import settings

from .utils import get_from_cache, set_cache, get_selector
from .models_permission import *

from logging import getLogger

AUTH_USER_MODEL = 'account.User'

from .models_common import *


_logger = getLogger(__name__)


DEFAULT_CACHE_TIMEOUT = settings.PERMISSION_CACHE_TIMEOUT


def get_userbased_pemissions(user, natural_key):
    key = "user:{}:{}".format(user.id, natural_key or "Default")
    result = get_from_cache(key)
    if not result:
        query = user.roles_set.filter(natural_key=natural_key)
        result = set_cache(key, query.all())
    return result


def get_groupbased_pemissions(selector, access_group_set):
    key = "group:{}:{}".format(str(access_group_set), selector)
    result = get_from_cache(key)
    if not result:
        query = GroupObjectRole.objects.filter(group_id__in=list(access_group_set), natural_key=selector)
        result = set_cache(key, query.all())
    return result


def is_permission_meets(mode, permission):
    severity = permission.severity
    bit = BaseObjectRole.ACTIONS.get(mode) or None
    return bool(severity & bit) if bit else False


def permission_ok(actual_permissions, mode, obj=None):
    if actual_permissions:
        for permission in actual_permissions:
            if is_permission_meets(mode, permission):
                if not obj or permission.check_objid(obj.id, mode):
                    return True
                else:
                    continue
    return False


def _check_permission_to_object(user, checked_permissions, obj):
    permission = checked_permissions[0] \
        if isinstance(checked_permissions, (list, tuple)) \
        else checked_permissions

    if permission.find(":") == -1:
        mode = permission
        selector = get_selector(obj)
    else:
        (selector, mode) = permission.split(":")
    restrictions = restricted_ids(user, obj or selector, mode)

    if not obj:
        return bool(restrictions)

    if not restrictions['+'] and not restrictions['-']:
        return restrictions['*']
    if restrictions['+']:
        return obj.id in restrictions['+'] and obj.id not in restrictions['-']
    if restrictions['-']:
        return obj.id not in restrictions['-']


def check_permission_to_object(user, checked_permissions, obj):
    if user.is_system_administrator:
        return True

    result = _check_permission_to_object(user, checked_permissions, obj)
    if result:
        _logger.debug("Object BASED PERMISSIONS OK. User: '{}'  to Object: '{}' ...{}".format(
            user, obj if obj else "*** ANY ***", checked_permissions))
    else:
        _logger.warning("Object BASED PERMISSIONS ERROR. User: '{}'  to Object: '{}' ...{}".format(
            user, obj if obj else "*** ANY ***", checked_permissions))

    return result


def scan_update(result, permissions, mode='read'):
    for p in permissions:
        if not is_permission_meets(mode, p):
            continue
        result['*'] = True

        objids = p.objids
        if objids.get(mode):
            objids = objids[mode]
            if objids:
                result['+'] = result['+'].union(objids['+'])
                result['-'] = result['-'].union(objids['-'])
    return result


def restricted_ids(user, model_or_selector, mode='read'):
    result = {
        '+': set(),
        '-': set(),
        '*': True
    }

    selector = model_or_selector if isinstance(model_or_selector, str) else get_selector(model_or_selector)
    access_group_set = {g.access_group_id for g in user.access_group_set.all()}

    scan_update(result, get_groupbased_pemissions(selector, access_group_set), mode)
    scan_update(result, get_userbased_pemissions(user, selector), mode)

    return result


def get_quireyset(user, model, mode='read'):
    from account.models_general import Organization
    from core.models import Project, UserProject

    if user.is_system_administrator or (mode == 'read' and user.is_system_auditor):
        return model.objects.all()

    selector = get_selector(model)

    public_ony_queryset = model.objects.none()

    organizations = [o.id for o in user.organizations.all()]
    if model == Project:
        public_ony_queryset = Project.objects.filter(public=True).all()
        projects1 = {o.id for o in Project.objects.filter(owner=user).all()}
        projects2 = {o.project_id for o in UserProject.objects.filter(user=user)}
        projects = list(projects1.union(projects2))
    else:
        projects = [o.id for o in user.projects.all()]
    access_group_set = {g.access_group_id for g in user.access_group_set.all()}

    queryset = model.objects.none()

    def __is_meet(permissions, mode, organizations):
        for p in permissions:
            if not (is_permission_meets(mode, p) and p.organization.id in organizations):
                continue
            else:
                return True
        return False

    def __owner_filter(model, user):
        if hasattr(model, 'owner'):
            return model.objects.filter(owner=user)
        else:
            return model.objects.none()

    group_based_perms = get_groupbased_pemissions(selector, access_group_set)
    user_based_perms = get_userbased_pemissions(user, selector)

    owner_filtered_queryset = __owner_filter(model, user)

    if __is_meet(group_based_perms, mode, organizations) \
    or __is_meet(user_based_perms, mode, organizations):
        if hasattr(model, 'project') and hasattr(model, 'organization'):
            queryset = model.objects.filter(project__in=projects) | model.objects.filter(organization__in=organizations)
        elif hasattr(model, 'project'):
            queryset = model.objects.filter(project__in=projects)
        elif hasattr(model, 'organization'):
            queryset = model.objects.filter(organization__in=organizations)
        elif model == Organization:
            queryset = model.objects.filter(id__in=organizations)
        elif model == Project:
            queryset = model.objects.filter(id__in=projects)
        else:
            queryset = model.objects.all()

    if queryset:
        queryset = queryset | owner_filtered_queryset | public_ony_queryset
    else:
        queryset = owner_filtered_queryset | public_ony_queryset

    return queryset

