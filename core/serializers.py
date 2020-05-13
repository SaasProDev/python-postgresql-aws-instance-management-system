# python
import copy
import json
import yaml
import logging
import operator
import re
import six
import urllib
from collections import OrderedDict
from datetime import timedelta

import yaml
import fcntl
try:
    import psutil
except Exception:
    psutil = None


from slugify import slugify, Slugify, UniqueSlugify




from rest_framework.reverse import reverse


from rest_framework import serializers

from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404



from core.models import *
from core.views import *


from core.utils import *

from frontend.urls import *

from ahome.base_serializer import BaseSerializer
from ahome.base_serializer import ProjectBaseSerializer
# from ahome.base_serializer import IaasBaseSerializer




def reverse_gfk(content_object, request):
    '''
    Computes a reverse for a GenericForeignKey field.
    Returns a dictionary of the form
        { '<type>': reverse(<type detail>) }
    for example
        { 'organization': '/api/v2/organizations/1/' }
    '''
    if content_object is None or not hasattr(content_object, 'get_absolute_url'):
        return {}

    return {
        camelcase_to_underscore(content_object.__class__.__name__): content_object.get_absolute_url(request=request)
    }




class RirSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Rir
        fields = '__all__'


class VrfSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Vrf
        fields = '__all__'


class PrefixSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Prefix
        fields = '__all__'



class VlanSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Vlan
        fields = '__all__'



class AggregateSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Aggregate
        fields = '__all__'



class IPAddressSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = IPAddress
        fields = '__all__'


class DeviceSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()

    # run = serializers.SerializerMethodField('_get_run_fields')

    class Meta:
        model = Device
        # fields = '__all__'
        exclude = ('facts', )

    # def _get_run_fields(self, obj):
    #     return {} if obj is None else self.get_run_fields(obj)


    # def get_run_fields(self, obj):

    #     run_fields = OrderedDict()
    #     run_fields['synchronize'] = reverse('device-run-synchronize', args=[obj.pk])
    #     run_fields['activate'] = reverse('device-run-activate', args=[obj.pk])
    #     run_fields['deactivate'] = reverse('device-run-deactivate', args=[obj.pk])
    #     run_fields['shutdown'] = reverse('device-run-shutdown', args=[obj.pk])
    #     run_fields['reconfigure'] = reverse('device-run-reconfigure', args=[obj.pk])

    #     # view.reverse_action('set-password', args=['1'])
    #     # view.reverse_action(view.DeviceViewSet.run_synchronize, args=[obj.pk])

    #     return run_fields









class NetworkGearSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = NetworkGear
        fields = '__all__'


class ContainerSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Container
        fields = '__all__'


class VirtualMachineSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    uuid = serializers.ReadOnlyField()

    # run = serializers.SerializerMethodField('_get_run_fields')


    class Meta:
        model = VirtualMachine
        # fields = '__all__'
        exclude = ('facts', 'definition' )

    # def _get_run_fields(self, obj):
    #     return {} if obj is None else self.get_run_fields(obj)


    # def get_run_fields(self, obj):

    #     run_fields = OrderedDict()
    #     run_fields['synchronize'] = reverse('virtualmachine-run-synchronize', args=[obj.pk])
    #     run_fields['activate'] = reverse('virtualmachine-run-activate', args=[obj.pk])
    #     run_fields['deactivate'] = reverse('virtualmachine-run-deactivate', args=[obj.pk])
    #     run_fields['shutdown'] = reverse('virtualmachine-run-shutdown', args=[obj.pk])
    #     run_fields['reconfigure'] = reverse('virtualmachine-run-reconfigure', args=[obj.pk])


    #     # view.reverse_action('set-password', args=['1'])
    #     # view.reverse_action(view.DeviceViewSet.run_synchronize, args=[obj.pk])

    #     return run_fields





class ProviderSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    uuid = serializers.ReadOnlyField()

    summarized_fields = serializers.SerializerMethodField('_get_summarized_fields')


    class Meta:
        model = Provider
        fields = '__all__'
        # exclude = ('facts', )


    def _get_summarized_fields(self, obj):
        return {} if obj is None else self.get_summarized_fields(obj)


    def get_summarized_fields(self, obj):
        summarized_fields = OrderedDict()
        # summarized_fields['iaas'] = IaaS.objects.filter(provider = obj.pk ).count()
        # summarized_fields['virtualmachine'] = VirtualMachine.objects.filter(iaas__provider = obj.pk ).count()
        summarized_fields['device'] = Device.objects.filter(provider = obj.pk ).count()
        return summarized_fields



# class IaaSSerializer(IaasBaseSerializer):
class IaaSSerializer(BaseSerializer):
    id = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()
    summarized_fields = serializers.SerializerMethodField('_get_summarized_fields')

    class Meta:
        model = IaaS
        exclude = ('facts', )

    def _get_summarized_fields(self, obj):
        return {} if obj is None else self.get_summarized_fields(obj)

    def get_summarized_fields(self, obj):
        summarized_fields = OrderedDict()
        summarized_fields['virtualmachine'] = VirtualMachine.objects.filter(iaas = obj.pk ).count()
        summarized_fields['failed_vm']      = VirtualMachine.objects.filter(iaas = obj.pk, status='failed').count()
        summarized_fields['running_vm']     = VirtualMachine.objects.filter(iaas = obj.pk, status='successful').count()
        return summarized_fields


class PaaSSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    uuid = serializers.ReadOnlyField()

    summarized_fields = serializers.SerializerMethodField('_get_summarized_fields')


    class Meta:
        model = PaaS
        # fields = '__all__'
        exclude = ('facts', )

    def _get_summarized_fields(self, obj):
        return {} if obj is None else self.get_summarized_fields(obj)


    def get_summarized_fields(self, obj):

        summarized_fields = OrderedDict()
        summarized_fields['virtualmachine'] = VirtualMachine.objects.filter( iaas = obj.pk ).count()
        summarized_fields['failed_vm'] = VirtualMachine.objects.filter( iaas = obj.pk, status='failed').count()
        summarized_fields['running_vm'] = VirtualMachine.objects.filter( iaas = obj.pk, status='successful').count()
        return summarized_fields




class UserCredentialSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    uuid = serializers.ReadOnlyField()

    summarized_fields = serializers.SerializerMethodField('_get_summarized_fields')


    class Meta:
        model = UserCredential
        # fields = '__all__'
        exclude = ('facts', )


    def _get_summarized_fields(self, obj):
        return {} if obj is None else self.get_summarized_fields(obj)


    def get_summarized_fields(self, obj):

        summarized_fields = OrderedDict()
        summarized_fields['iaas'] = IaaS.objects.filter(usercredential = obj.pk ).count()
        summarized_fields['virtualmachine'] = VirtualMachine.objects.filter(iaas__usercredential = obj.pk ).count()
        # summarized_fields['device'] = Device.objects.filter(provider = obj.pk ).count()

        return summarized_fields


class UserSecretSerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    uuid = serializers.ReadOnlyField()

    summarized_fields = serializers.SerializerMethodField('_get_summarized_fields')


    class Meta:
        model = UserSecret
        fields = '__all__'
        # exclude = ('facts', )


    def _get_summarized_fields(self, obj):
        return {} if obj is None else self.get_summarized_fields(obj)


    def get_summarized_fields(self, obj):

        summarized_fields = OrderedDict()
        # summarized_fields['iaas'] = IaaS.objects.filter(usercredential = obj.pk ).count()
        summarized_fields['virtualmachine'] = VirtualMachine.objects.filter(iaas__usercredential = obj.pk ).count()
        # summarized_fields['device'] = Device.objects.filter(provider = obj.pk ).count()

        return summarized_fields







class UserKeySerializer(BaseSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = UserKey
        fields = '__all__'



class SdnSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Sdn
        fields = '__all__'


class StorageSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Storage
        fields = '__all__'


class ServiceSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = '__all__'


class MonitoringSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Monitoring
        fields = '__all__'


class SecuritySerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Security
        fields = '__all__'


class PkiSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Pki
        fields = '__all__'


class BackupSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Backup
        fields = '__all__'


class BillingSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Billing
        fields = '__all__'


class DocumentationSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = Documentation
        fields = '__all__'



class JobSerializer(serializers.HyperlinkedModelSerializer):

    ident = serializers.ReadOnlyField()

    class Meta:
        model = Job
        fields = '__all__'


class JobEventSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = JobEvent
        # fields = '__all__'
        exclude = ('event_data', )


class RunnerTaskSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.ReadOnlyField()

    class Meta:
        model = RunnerTask
        fields = '__all__'


# class InfrastructureSerializer(serializers.HyperlinkedModelSerializer):
#     id   = serializers.ReadOnlyField()
#     uuid = serializers.ReadOnlyField()
#
#     class Meta:
#         model = Infrastructure
#         fields = '__all__'


# class ProjectSerializer(serializers.HyperlinkedModelSerializer):
class ProjectSerializer(ProjectBaseSerializer):
    id   = serializers.ReadOnlyField()
    uuid = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = '__all__'



class YourSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   comments = serializers.IntegerField()
   likes = serializers.IntegerField()

