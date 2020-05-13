
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _

import requests

from core.models import *
from django.shortcuts import render

from .functions import get_apidata

from django.contrib.auth.decorators import login_required
import pprint
from sysutils.utils.dict_utils import safeget

from .handlers.price_handler import counts_calculate, empty_billing_info

API_NAME = 'dashboard'



@login_required
def index(request):

    # apidata = get_apidata(API_NAME, request)
    # CONTEXT = { 'apidata': apidata, }

    # CONTEXT.update({ "{}_active".format(API_NAME): 'active', })
    
    # # if request.is_ajax():
    # #     return render(request, 'frontend/index.html', CONTEXT)

    # # return render(request, 'frontend/index.angularjs.html', CONTEXT)
    # # return render(request, 'frontend/includes/dashboard/index.html', CONTEXT)
    # return render(request, 'frontend/index.html', CONTEXT)
    # # return render(request, 'frontend/index3.html', CONTEXT)


    apidata = get_apidata(API_NAME, request)

    CONTEXT = {'apidata': apidata}
    CONTEXT.update({"{}_active".format(API_NAME): 'active'})
    info = empty_billing_info()

    usercredentials = get_apidata('usercredentials', request)
    usage           = get_apidata('userdashboard/virtualmachines/usage/list', request)
    virtualmachines = get_apidata('virtualmachines', request) or {}
    iaas            = get_apidata('iaas', request)

    # calculate(info['counts'], 'virtualmachines', virtualmachines.get('results', []))
    # calculate(info['counts'], 'iaas', iaas.get('results', []))

    counts_calculate(info['counts'], 'virtualmachines', virtualmachines.get('results', []), apply_billing=False)
    counts_calculate(info['counts'], 'iaas', iaas.get('results', []))

    # pprint.pprint(virtualmachines)
    # vmhosts = [
    #     {'name': "TEST 0", 'status': "successful", "ip": "127.0.0.1", "image": "IMAGE-1", 'webssh': "xxxx"},
    #     {'name': "TEST 1", 'status': "failed", "ip": "127.0.0.2", "image": "IMAGE-2", 'webssh': "xxxx"},
    # ]
    vmhosts = []
    for item in virtualmachines.get('results') or []:
        # dat = {}
        vm = {
            'ip': safeget(item, 'ipv4', 'address', default=""),
            'name': safeget(item, 'name', default="unknown"),
            'status': safeget(item, 'status', default="unknown"),
            'image': safeget(item, 'setfacts', 'image_id', default="unknown"),
            'iaas_image': safeget(item, 'summary_fields', 'iaas', 'inputs', 'image', default="{}"),

        }
        vmhosts.append(vm)

    data = dict(api=dict(
        info            = info,
        providers       = get_apidata('providers', request),
        usercredentials = usercredentials,
        usersecrets     = get_apidata('usersecrets', request),
        # imagegroups     = get_apidata('provisioning/iaac/image_groups/list', request),
        # plangroups      = get_apidata('provisioning/iaac/plan_groups/list', request),
        virtualmachines_usage   = usage,
        iaas            = iaas,
        virtualmachines = virtualmachines,
        vmhosts = vmhosts
    ))
    CONTEXT.update(data)
    # pprint.pprint(usage)
    return render(request, 'frontend/index.html', CONTEXT)

