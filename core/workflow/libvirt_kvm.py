from django.db import models
from django.conf import settings as django_settings

from core.constants import *
from core.fields import IPNetworkField, IPAddressField

from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import smart_str
from django.utils.timezone import now

import xmltodict, json

import uuid
import time
from datetime import datetime
# jsonschema
from jsonschema import Draft4Validator, FormatChecker
import jsonschema.exceptions

# Django-JSONField
from django.contrib.postgres.fields import JSONField
# from jsonfield import JSONField as upstream_JSONField

from core.models import * #noqa
# from core.tasks import *

#import netaddr

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def workflow_on_event_provider_libvirt_kvm( instance, **kwargs ):

	## Save device facts
	if instance.event == 'runner_on_ok':
	    if instance.namespace == 'Provider.libvirt':
	        # Gathering facts
	        if instance.event_data.get('task_action') == 'gather_facts' :
	            # Update Hypvervisors/Devices
	            obj, _ignore = Device.objects.update_or_create(
	                name = instance.event_data.get('host'),  fqdn = instance.event_data.get('remote_addr'),
	                defaults = {
	                    'facts': instance.event_data.get('res'),
	                    'ident': instance.runner_ident,
	                    },
	                )
	        if instance.event_data.get('task_action') == 'debug':
	            
	            if instance.event_data['res'].get('r__guests_xml'):

	                for vm in instance.event_data['res']['r__guests_xml']['results']:

	                    obj, _ignore = VirtualMachine.objects.update_or_create(
	                        name = vm.get('item'),  hosted = instance.event_data.get('host'),
	                        defaults = {
	                            'definition': json.dumps(xmltodict.parse(vm.get('get_xml'))),
	                            },
	                        )

	            if instance.event_data['res'].get('r__guests_status'):

	                for vm in instance.event_data['res']['r__guests_status']['results']:

	                    obj, _ignore = VirtualMachine.objects.update_or_create(
	                        name = vm.get('item'),  hosted = instance.event_data.get('host'),
	                        defaults = {
	                            'status': vm.get('status'),
	                            'kind': 'libvirt',
	                            },
	                        )

	            if instance.event_data['res'].get('r__netinfo'):

	                for network in instance.event_data['res']['r__netinfo']['networks']:

	                    obj, _ignore = Sdn.objects.update_or_create(
	                        name = network,  hosted = instance.event_data.get('host'),
	                        defaults = {
	                            'source': instance.event_data['res']['r__netinfo']['networks'][network],
	                            'kind': 'libvirt',
	                            },
	                        )





def save_device_libvirt_kvm(instance, **kwargs):
	pass


def save_virtual_machine_libvirt_kvm(instance, **kwargs):
	pass


def save_sdn_libvirt_kvm(instance, **kwargs):
	pass

def save_ip_address_libvirt_kvm(instance, **kwargs):
	pass

def save_prefix_libvirt_kvm(instance, **kwargs):
	pass


