import os
import json
import datetime
import time
from collections import OrderedDict
import netaddr

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers as core_serializers
from django.core.serializers import serialize
from django.forms.models import model_to_dict

# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, views, generics, status
from rest_framework.decorators import action
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login

import traceback
from logging import getLogger
from core.serializers import *

from django.core.serializers.json import DjangoJSONEncoder

from core.tasks import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import copy

from core.utils import *

from frontend.urls import *

from django.contrib.auth import get_user_model

from rest_framework.decorators import permission_classes
from account.permissions import DefaultRoleBasedPermissions
from account.base_viewset import DefaultPermittedBaseViewSet

# from rest_framework import views
# from rest_framework.response import Response
# from .serializers import YourSerializer
from core.utils import get_model_from_str, load_yml_to_dict, ahomefile_to_dict, dict_yaql, append_ahomefile_fields, ahomefile_yaql, get_ssh_version
import yaml


from .views_provision import *
from .views_dashboard import *

_logger = getLogger(__name__)

# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, YourCustomType):
#             return str(obj)
#         return super().default(obj)


## Health
def health(request):
    return JsonResponse({'status': 'ok'})


class PermittedViewSet(DefaultPermittedBaseViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields =     ['name', 'description']
    filterset_fields =  ['name', 'description']
    ordering_fields =   ['name']

    def _check_if_can_be_run(self, action):
        user = self.request.user
        obj = super().get_object()
        # _logger.warning("*** Run PERMISSION CHECKING FOR '{}' ***".format(obj))
        try:
            if not user.has_perms("execute", obj):
                 self.permission_denied(self.request, message="cannot perform '{}' action".format(action))
        except Exception as ex:
            _logger.warning("EXCEPTION DURING PERMISSION {}; SKIPPED".format(ex))
        return obj

    def _run(self, action=None, action_name=None):
        """ Starting a corresponded Async Celery Task """
        action_name = action_name or "{}ing".format(action or "Default Action").capitalize()
        model = None
        try:
            s = serialize('json', [self._check_if_can_be_run(action)])
            serializer = json.loads(s)

            instance = serializer[0]

            model = instance.get('model')
            pk    = instance.get('pk')
            uuid  = instance.get('fields').get('uuid')
            name  = instance.get('fields').get('name')

            # Create entry for the Runner Task Workflow - applications

            # TODO: Duplicated code for now - signals.py
            f_applications  = instance.get('fields').get('applications')
            if f_applications:
                pass
                # TEMP FOR TESTING PURPOSE ONLY - HARDCODED APPS
                # if model in ['core.iaas']:                
                #     t = IaaS.objects.get(id = pk)
                #     t.applications = ['apache', 'docker']
                #     t.save()

                _logger.info(f"RunnerTasks : -- {f_applications}")
                entry = dict(
                    obj    = model,
                    obj_id = pk,
                    state  = 'NewApp',
                    ident  = uuid,  
                    )
                runner_obj = RunnerTask.objects.filter( **entry )
                if not runner_obj:
                    RunnerTask.objects.create(**entry)

            ## -- end
            
            params = dict(instance=instance, action=action) if action \
                else dict(instance=instance)
            task = RunActivateJob1.delay(**params)

            return Response(
                {'status': '{} in progress on model: {}, name: {}, uuid: {}'.format(
                    action_name, model, name, uuid)})

        except ObjectDoesNotExist as ex:
            _logger.warning("Cannot perform '{}' for model: '{}'; Exception: {};{} SKIPPED".format(
                action_name, model, ex, traceback.format_exc()))

            return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=['post', 'get'], detail=True)
    def run_check(self, request, pk=None):
        return self._run('check', "Synchronization")

    @action(methods=['post', 'get'], detail=True)
    def run_synchronize(self, request, pk=None):
        return self._run('check', 'Synchronization')

    @action(methods=['post', 'get'], detail=True )
    def run_activate(self, request, pk=None):
        return self._run('start', 'Activation')

    @action(methods=['post', 'get'], detail=True)
    # @action(methods=['post'], detail=True)
    def run_deactivate(self, request, pk=None):
        return self._run('stop', 'Deactivation')

    @action(methods=['post', 'get'], detail=True)
    def run_reconfigure(self, request, pk=None):
        return self._run('reconfigure', 'Reconfiguration')

    @action(methods=['post', 'get'], detail=True)
    def run_shutdown(self, request, pk=None):
        return self._run('stop', 'Shutting down')

    @action(methods=['post', 'get'], detail=True)
    def run_deployment(self, request, pk=None):
        return self._run('deploy', 'Deployment')

    @action(methods=['post', 'get'], detail=True)
    def run_decommission(self, request, pk=None):
        return self._run('remove', 'Decommission')


## Rir ViewSet
class RirViewSet(viewsets.ModelViewSet):
    queryset = Rir.objects.all()
    serializer_class = RirSerializer


## Vrf ViewSet
class VrfViewSet(viewsets.ModelViewSet):
    queryset = Vrf.objects.all()
    serializer_class = VrfSerializer


## Prefix ViewSet
class PrefixViewSet(viewsets.ModelViewSet):
    queryset = Prefix.objects.all()
    serializer_class = PrefixSerializer


## Vlan ViewSet
class VlanViewSet(viewsets.ModelViewSet):
    queryset = Vlan.objects.all()
    serializer_class = VlanSerializer


## Aggregate ViewSet
class AggregateViewSet(viewsets.ModelViewSet):
    queryset = Aggregate.objects.all()
    serializer_class = AggregateSerializer


## IPAddress ViewSet
class IPAddressViewSet(viewsets.ModelViewSet):
    queryset = IPAddress.objects.all()
    serializer_class = IPAddressSerializer


## Device ViewSet
class DeviceViewSet(PermittedViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


## Container ViewSet
class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


## VirtualMachine ViewSet
class VirtualMachineViewSet(PermittedViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

    search_fields =     ['name', 'description', ]
    filterset_fields =  ['id', 'iaas', 'project']
    ordering_fields =   ['name', ]


## NetworkGear ViewSet
class NetworkGearViewSet(viewsets.ModelViewSet):
    queryset = NetworkGear.objects.all()
    serializer_class = NetworkGearSerializer


## Provider ViewSet
class ProviderViewSet(PermittedViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    ordering_fields = ['name', ]

## IaaS ViewSet
class IaaSViewSet(PermittedViewSet):
    queryset = IaaS.objects.all()
    serializer_class = IaaSSerializer

    search_fields =     ['name', 'description', ]
    # filterset_fields =  ['id', 'usercredential', 'infrastructure']
    filterset_fields =  ['id', 'usercredential', 'iaas']
    ordering_fields =   ['name', ]

    @action(methods=['post'], detail=True, )
    def run_deploy(self, request, pk=None):
        return self._run(None, "Activation")


## PaaS ViewSet
class PaaSViewSet(PermittedViewSet):
    queryset = PaaS.objects.all()
    serializer_class = PaaSSerializer

    search_fields =     ['name', 'description', ]
    # filterset_fields =  ['id', 'usercredential', 'infrastructure']
    filterset_fields =  ['id', 'usercredential', 'iaas']
    ordering_fields =   ['name', ]

    @action(methods=['post'], detail=True, )
    def run_deploy(self, request, pk=None):
        return self._run(None, "Activation")


class SdnViewSet(DefaultPermittedBaseViewSet):
    queryset = Sdn.objects.all()
    serializer_class = SdnSerializer


class StorageViewSet(DefaultPermittedBaseViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer


class ServiceViewSet(DefaultPermittedBaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


## Monitoring ViewSet
class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer


## Security ViewSet
class SecurityViewSet(viewsets.ModelViewSet):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer


## Pki ViewSet
class PkiViewSet(viewsets.ModelViewSet):
    queryset = Pki.objects.all()
    serializer_class = PkiSerializer


## Backup ViewSet
class BackupViewSet(viewsets.ModelViewSet):
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer


## Billing ViewSet
class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer


## Documentation ViewSet
class DocumentationViewSet(viewsets.ModelViewSet):
    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer


## Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


## JobEvent ViewSet
class JobEventViewSet(viewsets.ModelViewSet):
    queryset = JobEvent.objects.all()
    serializer_class = JobEventSerializer


## UserCredentials ViewSet
class UserCredentialViewSet(PermittedViewSet):
    queryset = UserCredential.objects.all()
    serializer_class = UserCredentialSerializer


## UserSecrets ViewSet
class UserSecretViewSet(PermittedViewSet):
    queryset = UserSecret.objects.all()
    serializer_class = UserSecretSerializer


## UserKeys ViewSet
class UserKeyViewSet(PermittedViewSet):
    queryset = UserKey.objects.all()
    serializer_class = UserKeySerializer


## RunnerTasks ViewSet
class RunnerTaskViewSet(viewsets.ModelViewSet):
    queryset = RunnerTask.objects.all()
    serializer_class = RunnerTaskSerializer


# ## Configuration ViewSet
# class ConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = Configuration.objects.all()
#     serializer_class = ConfigurationSerializer

# class InfrastructureViewSet(viewsets.ModelViewSet):
#     queryset = Infrastructure.objects.all()
#     serializer_class = InfrastructureSerializer

class ProjectViewSet(DefaultPermittedBaseViewSet):
# class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class WizardBoxesViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):

        related_fields = OrderedDict()

        # Provider
        r__values = Provider.objects.all().values()

        r__fields = []

        for rval in r__values:
            r__dict = OrderedDict(
                name=rval.get("name"),
                id=rval.get("id"),
                kind=rval.get("kind"),
                # url = "",
                # "{% url 'wizardboxesform_generate' 'ec2' 'provider' provider.id %}"
                subs=[],
                icon=DICT_PROVIDER_ICONS.get(rval.get("kind", "fa fa-cloud")),
                runner=rval.get("runner"),
            )

            if rval.get("kind") in DICT_PROVIDER_KINDS.keys():
                map__data = DICT_PROVIDER_KINDS[rval.get("kind")]
                r__subs = []
                for r__sub in map__data:
                    r__subs.append(OrderedDict(
                        name=r__sub.get("name"),
                        label=r__sub.get("label"),
                        wizardboxesform=reverse('wizardboxesform_generate',
                                                args=[r__sub.get("name"), 'provider', rval.get("id")]),
                        icon=r__sub.get("icon"),
                    )
                    )

                r__dict.update({"subs": r__subs})

            r__fields.append(r__dict)

        related_fields['provider'] = r__fields

        return Response(related_fields)

    def retrieve(self, request, pk=None):
        pass

    # def update(self, request, pk=None):
    #     pass
    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


def dashboard_entry(user, cls):
    quireyset = user.get_available_objects(cls, mode='read')
    count = quireyset.count()
    return dict(total=count, critical=0, warning=0)


class DashboardViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        user = request.user

        data = OrderedDict()
        data['summaries'] = dict( 
                organizations   = dashboard_entry(user, Organization),
                sdn             = dashboard_entry(user, Sdn),
                ipaddresses     = dashboard_entry(user, IPAddress),
                prefixes        = dashboard_entry(user, Prefix),
                devices         = dashboard_entry(user, Device),
                networkgears    = dashboard_entry(user, NetworkGear),
                rir             = dashboard_entry(user, Rir),
                vlans           = dashboard_entry(user, Vlan),
                vrf             = dashboard_entry(user, Vrf),
                virtualmachines = dashboard_entry(user, VirtualMachine),
                jobs            = dashboard_entry(user, Job),
                events          = dashboard_entry(user, JobEvent),
                providers       = dashboard_entry(user, Provider),
                storages        = dashboard_entry(user, Storage)
             )
        #sio.emit("notifications", {'data': "****** UUUUUUUUU ********"})
        return Response(data)

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass



class ProvisioningViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        user = request.user

        data = OrderedDict()
        data['iaac'] = dict( 
                organizations   = dashboard_entry(user, Organization),
                sdn             = dashboard_entry(user, Sdn),
                ipaddresses     = dashboard_entry(user, IPAddress),
                prefixes        = dashboard_entry(user, Prefix),
                devices         = dashboard_entry(user, Device),
                networkgears    = dashboard_entry(user, NetworkGear),
                rir             = dashboard_entry(user, Rir),
                vlans           = dashboard_entry(user, Vlan),
                vrf             = dashboard_entry(user, Vrf),
                virtualmachines = dashboard_entry(user, VirtualMachine),
                jobs            = dashboard_entry(user, Job),
                events          = dashboard_entry(user, JobEvent),
                providers       = dashboard_entry(user, Provider),
                storages        = dashboard_entry(user, Storage)
             )
        return Response(data)

    def retrieve(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
