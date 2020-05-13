from django.shortcuts import render, get_object_or_404
from .functions import OPS, get_apidata, save_form
import pprint
from django.contrib.auth.decorators import login_required
from sysutils.utils.dict_utils import safeget
from logging import getLogger

from .handlers.price_handler import counts_calculate, empty_billing_info

API_NAME = 'dashboard'

_logger = getLogger(__name__)


@login_required
def dashboard(request):
    apidata = get_apidata(API_NAME, request)
    CONTEXT = {'apidata': apidata,}
    CONTEXT.update({"{}_active".format(API_NAME): 'active', })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)


@login_required
def dashboard_user(request):
    apidata = get_apidata(API_NAME, request)

    CONTEXT = {'apidata': apidata}
    CONTEXT.update({"{}_active".format(API_NAME): 'active'})

    info = empty_billing_info()

    usercredentials = get_apidata('usercredentials', request)
    usage           = get_apidata('userdashboard/virtualmachines/usage/list', request)
    virtualmachines = get_apidata('virtualmachines', request)
    iaas            = get_apidata('iaas', request)

    counts_calculate(info['counts'], 'virtualmachines', virtualmachines.get('results', []), apply_billing=False)
    counts_calculate(info['counts'], 'iaas', virtualmachines.get('results', []))

    _logger.debug("SUMMUP INFO for '{}' is: {}".format(API_NAME, pprint.pformat(info['counts'])))

    vmhosts = []
    for item in virtualmachines['results']:
        vm = {
            'ip': safeget(item, 'ipv4', 'address', default=""),
            'uuid': safeget(item, 'uuid', default=""),
            'id': safeget(item, 'id', default=-1),
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
        virtualmachines_usage  = usage,
        iaas            = iaas,
        virtualmachines = virtualmachines,
        vmhosts = vmhosts
    ))
    CONTEXT.update(data)
    # pprint.pprint(virtualmachines)
    # pprint.pprint(iaas)
    return render(request, 'frontend/includes/%s/user.html' % API_NAME, CONTEXT)
