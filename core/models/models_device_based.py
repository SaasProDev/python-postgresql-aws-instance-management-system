import copy
import traceback
import logging
import pprint
from django.db import models
from django.conf import settings
from .base_device_models import DeviceTemplate
from .models_job_based import IaaS, UserCredential
import json


_logger = logging.getLogger(__name__)

from sysutils.utils.dict_utils import safeget
# IaaS create data example - 3 Instances
# f-modal-image: {'image_id': 2, 'name': 'debian', 'label': 'Debian', 'iconClass': 'ahome/assets/debian-icon.svg', 'default': '18 x64', 'version': ['18 x64', '16 x64', '14 x64'], 'group_id': 1}
# f-modal-image-version: 18 x64
# f-modal-provider: 2
# f-modal-provider-name: RESGII REAL
# f-modal-provider-kind: amazon_ec2
# f-modal-plan: {'plan_id': 1, 'name': '1vcpu_1gb_60gb', 'price': 0.006, 'rate': 'hour', 'vcpu': 1, 'memory': 2, 'disk': 60, 'traffic': 'unlimited traffic', 'currency': 'euro'}
# f-modal-storage: {'storage_id': 2, 'name': 'disk_ssd_1000gb', 'price': 0.05, 'rate': 'hour', 'disk': 1000, 'unit': 'GB', 'type': 'SSD', 'currency': 'euro'}
# f-modal-authentication-key:
# f-modal-authentication-secret:
# f-modal-project:
# f-modal-name: 23-2J
# f-modal-instance: 23-2
# f-modal-count: 3
# f-modal-tags:
# f-modal-costs: 122.64

# 'billing': {
#     'total': 0,
#     'rate_month': 0
# }

# return {
#     'currency': 'euro',
#     'total': max(round(hour_rate, 4), round(total, 2)),
#     'current': max(round(hour_rate, 4), round(total, 2)),
#     'rate_month': cost,
#     'live_time': live_time,
#     'rate_hour': round(hour_rate, 4),  # todo - update formula - based on summup inluded resources
# }


HOURS_IN_MONTH = settings.HOURS_IN_MONTH
HOURS_IN_DAY = 24
DEFAULT_CURRENCY = 'dollar'


def _extract_price(item):
    currency = item.get('currency') or DEFAULT_CURRENCY
    price = float(item.get('price'))or 0
    rate = item.get('rate') or 'hour'
    hour_rate = 0

    if rate.lower() == 'hour':  hour_rate = price
    if rate.lower() == 'day':   hour_rate = price / HOURS_IN_DAY
    if rate.lower() == 'month': hour_rate = price / HOURS_IN_MONTH

    return {
        'currency': currency,
        'rate_hour': hour_rate,
        'rate_month': price if rate.lower() == 'month' else HOURS_IN_MONTH * hour_rate,
        'current': 0,
        'total': 0,
        'live_time': 0
    }


def _price_summ(a, b):
    if a['currency'] != b['currency']:
        #raise Exception("Only THE SAME Currency for price supported now")
        _logger.warning("DIFFERENT CURENCY {}/{}... SKIPPED".format(a, b))
    result = {}
    for name in ['rate_month', 'total', 'rate_hour', 'current']:
        result[name] = a[name] + b[name]
    return result


def prppogate_billing_info(inputs):
    #plan = json.loads(inputs.get('plan', "")) or {}
    try:
        plan = inputs.get('plan', "")
        storage_str = inputs.get('storage', "{}")
        # _logger.debug("PLAN {} {}".format(type(plan), pprint.pformat(plan)))
        _logger.debug("STORAGE 1 {} {}".format(type(storage_str), pprint.pformat(storage_str)))
        storage = json.loads(storage_str.replace('\'','\"'))  # todo - should be more smart
        # _logger.debug("STORAGE 2 {} {}".format(type(storage), pprint.pformat(storage)))

        billing = _price_summ(_extract_price(plan), _extract_price(storage))
        _logger.debug("BILLING {}".format(pprint.pformat(billing)))
        cost = billing['rate_hour']
    except Exception as ex:
        _logger.error("CANNOT PARSE PLAN FOR IAAS, {} {}".format(ex, traceback.format_exc()))
        cost = 0
    return cost


class VirtualMachineManager(models.Manager):

    @staticmethod
    def cost_calculating(inputs):
        cost = prppogate_billing_info(inputs)
        return cost

    def create(self, **data):
        iaas = data.get('iaas')
        data['cost'] = self.cost_calculating(iaas.inputs)
        data['project'] = iaas.project
        # data['applications'] = iaas.applications
        _logger.debug("DATA STORED to VM {}".format(pprint.pformat(data, indent=4)))
        return super().create(**data)


class VirtualMachine(DeviceTemplate):
    """
    Virtual Machines
    """
    objects = VirtualMachineManager()

    iaas            = models.ForeignKey(IaaS, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    usercredential  = models.ForeignKey(UserCredential, related_name='%(class)ss', on_delete=models.PROTECT, blank=True, null=True)
    cost            = models.FloatField(default=0.0)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.applications:
            dataset = IaaS.objects.filter(virtualmachines__uuid=self.uuid)
            for ds in dataset:
                self.applications = ds.applications
        return super().save(*args, **kwargs)


class NetworkGear(DeviceTemplate):
    """
    Network Gears
    """
    class Meta:
        ordering = ['name',]

    def __str__(self):
        return str(self.name)

