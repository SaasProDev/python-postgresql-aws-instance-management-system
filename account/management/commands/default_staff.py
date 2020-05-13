import copy
import sys
import traceback
from django.core.management.base import BaseCommand

from django.conf import settings
from account.models import (User,
                            UserOrganizations,
                            AccessGroup,
                            AccessGroups,
                            Organization,
                            Team,
                            UserObjectRole,
                            GroupObjectRole)


import account.models
import core.models
from core.models import Provider, Project, IaaS
from core.constants import LOCAL_PROVIDERS_CHOICES, CLOUD_PROVIDER_CHOICES

from account.models import FULL_ACCESS_PERMISSION, READ_ONLY_PERMISSION


DEFAULT_ORGANISATION_DATA = {
    'name': settings.DEFAULT_ORGANISATION_NAME,
    'description' : "General Organisation for simple Users",
    'location': "",
    'contact': "",
    'phone': "",
    'email': "",
    'info': "",
    'status': "DEFAULT",
    'kind': "stub"
}

DEFAULT_PROJECT_DATA = {
    'name': settings.DEFAULT_PROJECT_NAME,
    'description': "Default Project - the mostly for tests :)",
    'public': True
}

DEFAULT_INFRASTRUCTURE_DATA = {
    'name': "Initial Infrastructure",
    'description': "The Initial Infrastructure"
}


DEFAULT_TEAM_DATA = {
    'name': "Whole General",
    'description': "Default Team"
}


def check_create_organization():
    try:
        organization = Organization.objects.create(**DEFAULT_ORGANISATION_DATA)
    except:
        organization = Organization.objects.filter(name=DEFAULT_ORGANISATION_DATA['name']).first()
    return organization


def check_create_project(organization, user):
    try:
        project = Project.create(organization=organization, user=user, **DEFAULT_PROJECT_DATA)
    except:
        project = Project.objects.filter(organization=organization, name=DEFAULT_PROJECT_DATA['name']).first()
    return project


# def check_create_infrastructure(project):
#     infrastructure = IaaS.objects.filter(name=DEFAULT_INFRASTRUCTURE_DATA['name']).first()
#     if not infrastructure:
#         infrastructure = IaaS.objects.create(project=project, **DEFAULT_INFRASTRUCTURE_DATA)
#     return infrastructure


# def insert_providers():
#     try:
#         for (name, description) in LOCAL_PROVIDERS_CHOICES:
#             Provider.objects.create(name=name, description=description, kind="local")
#
#         for (name, description) in CLOUD_PROVIDER_CHOICES:
#             Provider.objects.create(name=name, description=description, kind="cloud").first()
#     except:
#         print("Providers already in DB")
#         pass
#
#     try:
#         test_provider = Provider.objects.create(name="Test", description="Test Provider", kind="test")
#     except:
#         test_provider = Provider.objects.filter(kind="test").first()
#     return test_provider


def create_team(organization):
    data = copy.deepcopy(DEFAULT_TEAM_DATA)
    data['organization'] = organization
    try:
        return Team.objects.create(**data)
    except:
        return Team.objects.filter(name=DEFAULT_TEAM_DATA['name']).first()


def object_access_rule(organization, user):
    UserObjectRole.objects.create(user, organization, FULL_ACCESS_PERMISSION, user, "MANUAL-SET_UP")


class Command(BaseCommand):
    help = 'Default Staff Setup'

    def handle(self, *args, **options):
        organization = check_create_organization()

        user_user   = User.objects.get(pk=3)
        user_writer = User.objects.get(pk=4)

        project = check_create_project(organization, user_writer)
        print("Project: '{}' FIND / CREATED".format(project))

        team = create_team(organization)

        try:
            access_group = AccessGroup.objects.create(name="Read Access", organization=organization)
        except:
            access_group = AccessGroup.objects.filter(name="Read Access").first()

        try:
            full_access_group = AccessGroup.objects.create(name="Full Access", organization=organization)
        except:
            full_access_group = AccessGroup.objects.filter(name="Full Access").first()

        try:
            AccessGroups.objects.create(user=user_user, access_group=access_group)
        except Exception as ex:
            print("EXCEPTION SKIPPED FOR NOW - access_group error")

        try:
            AccessGroups.objects.create(user=user_writer, access_group=full_access_group)

        except Exception as ex:
            print("EXCEPTION SKIPPED FOR NOW - full_access_group error")


        ACCOUNT_MODELS  = account.models.IMPORTANT_MODELS
        CORE_MODELS     = core.models.IMPORTANT_MODELS

        for model in ACCOUNT_MODELS:
            GroupObjectRole.objects.create(access_group, organization, READ_ONLY_PERMISSION, model)
            print("Created {}".format(model.__name__))

        print()
        for model in CORE_MODELS:
            GroupObjectRole.objects.create(access_group, organization, READ_ONLY_PERMISSION, model)
            print("Created {}".format(model.__name__))

        print()
        for model in ACCOUNT_MODELS:
            GroupObjectRole.objects.create(full_access_group, organization, FULL_ACCESS_PERMISSION, model)
            print("Created {}".format(model.__name__))

        print()
        for model in CORE_MODELS:
            GroupObjectRole.objects.create(full_access_group, organization, FULL_ACCESS_PERMISSION, model)
            print("Created {}".format(model.__name__))



