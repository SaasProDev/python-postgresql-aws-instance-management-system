from ..models_general import *
from ..models_permission import *
from django.contrib.auth.models import Group, Permission

IMPORTANT_MODELS = (
    User,
    Team,
    UserOrganizations,
    AccessGroup,
    AccessGroups,
    Organization,
    UserObjectRole,
    GroupObjectRole
)