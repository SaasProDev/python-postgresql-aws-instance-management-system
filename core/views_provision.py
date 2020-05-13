from rest_framework.decorators import action
from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.conf import settings
from core.serializers import *
from frontend.urls import *


from core.utils import ahomefile_to_dict, dict_yaql
import yaml


_logger = getLogger(__name__)


PROVISIONING_DATA = "provisioning/data"

# DEFAULT_CACHE_TIME = settings.DEFAULT_CACHE_TIME
DEFAULT_CACHE_TIME = 60 * 20


# class YourView(views.APIView):
#
#     def get(self, request, *args, **kwargs):
#         yourdata = [{"likes": 10, "comments": 0}, {"likes": 4, "comments": 23}]
#         results = YourSerializer(yourdata, many=True).data
#         # return Response(results)
#
#         data = ahomefile_to_dict(PROVISIONING_DATA)
#         # query = "$.customers.orders.selectMany($.where($.order_id = 4))"
#         query = "$.image_groups"
#         qs = dict_yaql(data, query)
#         return Response(qs)


def ProvisioningIaac(query='$'):
    data = ahomefile_to_dict(PROVISIONING_DATA)
    qs = dict_yaql(data, query)
    return qs
    # return Response({ 'query': query, 'results': qs })


# Debug purpose only
def _ProvisioningIaac(query='$'):
    data = ahomefile_to_dict(PROVISIONING_DATA)
    qs = dict_yaql(data, query)
    # return Response(qs)
    return Response({'query': query, 'results': qs})


class ProvisioningIaacImageGroupsViewSet(views.APIView):
    # @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def get(self, request, *args, **kwargs):
        sql = "$.image_groups"
        return Response(ProvisioningIaac(sql))


class ProvisioningIaacImagesViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    # @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def list(self, request, group=None):
        sql = "$.image_groups.where($.group_name={}).select($.group_id).first()".format(group)
        group_id = ProvisioningIaac(sql)

        sql = "$.images.where($.group_id={})".format(group_id)
        return Response(ProvisioningIaac(sql))


class ProvisioningIaacPlanGroupsViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        sql = "$.plan_groups"
        return Response(ProvisioningIaac(sql))


class ProvisioningIaacPlansViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    # @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def list(self, request, provider=None, plan=None):
        sql = f"$.plan_groups.where($.plan_name={plan}).select($.plan_id).first()"
        plan_id = ProvisioningIaac(sql)

        sql = f"$.pricing.where($.provider={provider}).selectMany($.plans).where($.plan_id={plan_id})"
        return Response(ProvisioningIaac(sql))


class ProvisioningIaacStoragesViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    # @method_decorator(cache_page(DEFAULT_CACHE_TIME))
    def list(self, request, provider=None):
        sql = f"$.additional_storage.where($.provider={provider}).select($.plans).first()"
        provider_output = ProvisioningIaac(sql)
        return Response(provider_output)


