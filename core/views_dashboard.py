from rest_framework.decorators import action
from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.conf import settings
from core.serializers import *
from frontend.urls import *


from core.utils import ahomefile_to_dict, dict_yaql
import yaml


_logger = getLogger(__name__)


# PROVISIONING_DATA = "provisioning/data"

# DEFAULT_CACHE_TIME = settings.DEFAULT_CACHE_TIME
DEFAULT_CACHE_TIME = 60 * 20




class DashboardVirtualMachineStorageUsageViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    # @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def list(self, request):
        user = request.user

        qs = []
        unit = 1024*1024*1024
        for vm in user.get_available_objects(VirtualMachine, mode='read'):
            mounts = vm.mounts
            disk_root_usage_gb = 0
            disk_root_total_gb = 0
            disk_root_available_gb = 0

            for disk in mounts:
                if disk.get('mount') == '/':
                    size_total = disk.get('size_total', 0)
                    size_available = disk.get('size_available', 0)
                    
                    disk_root_usage_gb = (size_total - size_available)/(unit)
                    disk_root_total_gb = size_total/unit

            qs.append(
                dict(
                    name = vm.name,
                    inventory = vm.inputs.get('inventory'),
                    disk_root_usage_gb     = disk_root_usage_gb,
                    disk_root_total_gb     = disk_root_total_gb,
                    disk_root_available_gb = (disk_root_total_gb - disk_root_usage_gb),
                    disk_root_usage_percentage = (disk_root_usage_gb/disk_root_total_gb)*100 if disk_root_total_gb>0 else 0,
                    disk_root_available_percentage = ((disk_root_total_gb - disk_root_usage_gb)/disk_root_total_gb)*100 if disk_root_total_gb>0 else 0,
                    disk_root_css = 'progress-bar-success',  # warning # success # danger
                    )
                )

        return Response(qs)
