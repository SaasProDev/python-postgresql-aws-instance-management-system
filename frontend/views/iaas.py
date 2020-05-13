import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _

import requests

from core.models import IaaS
from core.utils.sshkeys_utils import get_or_build_sshkey
from sysutils.utils.dict_utils import safeget
from sysutils.utils.json_tools import json_write, json_loads
from sysutils.utils.file_utils import check_or_create_folder

from frontend.forms import *

from django.apps import apps
from django.conf import settings
from .functions import OPS, get_apidata, save_form

from frontend.forms import IaaSForm as ahomeForm
from django.contrib.auth.decorators import login_required
from pprint import pprint

import logging

_logger = logging.getLogger(__name__)

# from frontend.forms import CustomForm as ahomeForm
# from frontend.forms import CustomForm as ahomeJsonForm

# from django_jsonforms.forms import JSONSchemaForm

# formJson = JSONSchemaForm(schema=first_name_schema , options=options , ajax=False)

DEFAULT_CACHE_TIME = settings.DEFAULT_CACHE_TIME

from frontend.forms import get_form as ahomeWizardForm


jsonform = """
[{
        "name": "firstname",
        "label": "First Name",
        "type": "text",
        "max_length": 25,
        "required": 1,
        "help_text": "Enter your First Name"
    },
    {
        "name": "lastname",
        "label": "Last Name",
        "type": "text",
        "max_length": 25,
        "required": 1,
        "help_text": "Enter your Last Name"
    },
    {
        "name": "age",
        "label": "Age",
        "type": "integer",
        "max_value": 200,
        "min_value": 0,
        "help_text": "Enter your Age"
    },
    {
        "name": "internet",
        "label": "Internet Access",
        "type": "checkbox",
        "help_text": "Do you have an Internet Connection at home?"
    },
    {
        "name": "occupation",
        "label": "Occupation",
        "help_text": "Select your current occupation",
        "type": "select",
        "choices": [{
                "name": "Farmer",
                "value": "farmer"
            },
            {
                "name": "Engineer",
                "value": "engineer"
            },
            {
                "name": "Teacher",
                "value": "teacher"
            },
            {
                "name": "Office Clerk",
                "value": "office_clerk"
            },
            {
                "name": "Merchant",
                "value": "merchant"
            },
            {
                "name": "Unemployed",
                "value": "unemployed"
            },
            {
                "name": "Retired",
                "value": "retired"
            },
            {
                "name": "Other",
                "value": "other"
            }
        ]
    }

]
"""







API_NAME = 'iaas'
MODEL_NAME = 'IaaS'
MODEL_OBJ = IaaS


URL_CREATE = 'iaas_wizardbox_create' #'%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
# CONTEXT = { 'api_name': API_NAME, 'model_name': MODEL_NAME, 'include_path': INCLUDE_PATH, 'url_create': URL_CREATE, 'url_update': URL_UPDATE, 'url_delete': URL_DELETE, 'wizardform': WizardForm(prefix='wizard', jsonform=jsonform, initial={'firstname': 'Afahounko', 'lastname': 'Danny', 'age': 37, 'occupation': 'engineer'}), }

CONTEXT = dict(
    api_name = API_NAME,
    model_name = MODEL_NAME,
    include_path = INCLUDE_PATH,
    url_create = URL_CREATE,
    url_update = URL_UPDATE,
    url_delete = URL_DELETE,
    wizardboxform = WizardForm ( prefix='wizard', jsonform=jsonform, initial = { 'firstname': 'Afahounko', 'lastname': 'Danny', 'age': 37, 'occupation': 'engineer' }),
    )

CONTEXT.update({"{}_active".format(API_NAME): 'active'})

# todo FIX - LOGIN REQUIRED!
@login_required
def iaas_vmconnect(request):
    WEBSSH_BASE_URL = settings.WEBSSH_BASE_URL
    uuid = request.GET.get('uuid') if request.GET else request.POST.get('uuid')

    if uuid:
        _logger.debug("Starting WEB SSH Based on UUID...")
        url = "{}start?uuid={}".format(WEBSSH_BASE_URL, uuid)
        result = {"uuid": uuid}
    else:
        _logger.debug("Starting WEB SSH Based on USER/HOSTNAME...")
        # todo refactor
        user = request.GET.get('user') if request.GET else request.POST.get('user')
        host = request.GET.get('host') if request.GET else request.POST.get('host')
        url = "{}start?user={}&host={}".format(WEBSSH_BASE_URL, user, host)
        result = {"uuid": '', 'host': host}

    # url = "{}start?uuid={}".format(WEBSSH_BASE_URL, uuid)
    _logger.debug("Starting WEB SSH: '{}' ...".format(url))

    response = requests.get(url)
    _logger.debug("RESPONSE '{}'".format(response))

    if response.status_code == 200:
        data = json_loads(response.content)
        result['connect'] = data.get('connect')
        result['status'] = data.get('status')
    else:
        result['status'] = "ERROR"
    _logger.debug("VM Connect request. Result: {}".format(result))
    return JsonResponse(result)


@login_required
def iaas(request):
    wizardboxes_fields = get_apidata("wizardboxes", request)

    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields})
    CONTEXT.update({'request': request, })

    _logger.info("{} REQ".format(API_NAME), CONTEXT)
    #pprint(CONTEXT, indent=4)

    # TEMP_FOLDER     = settings.AHOME_PROOT_BASE_PATH
    SSH_STORE_FOLDER = settings.AHOME_SSKEYROOT_BASE_PATH
    VM_STORE_FOLDER  = settings.AHOME_VM_INFO_FOLDER

    check_or_create_folder(SSH_STORE_FOLDER)
    check_or_create_folder(VM_STORE_FOLDER)

    # todo caching apply
    for iaas_data in CONTEXT['apidata']['results']:
        iaas_data = dict(iaas_data)
        sored_keys = get_or_build_sshkey(iaas_data, SSH_STORE_FOLDER)
        keyfile = safeget(sored_keys, 'credentials', 'ssh_key')
        try:
            uuname = keyfile[len(SSH_STORE_FOLDER) + 1:]
        except Exception as ex:
            _logger.error("**** PLEASEFIX ME ***")
            uuname = "1234567-9999"
            keyfile = "88992121"

        iaas_data["uuname"] = uuname
        iaas_data["vm"] = []
        for vm in safeget(iaas_data, 'related', 'virtualmachine', default=tuple()):
            vm = VirtualMachine.objects.get(pk=vm['id'])
            data = vm.inputs
            data.update({'id': vm.id, "uuid": vm.uuid})
            data['ssh_key'] = keyfile

            vm_info_file_name = os.path.join(VM_STORE_FOLDER, "vm.{}.json".format(vm.uuid))
            json_write(vm_info_file_name, data)

            _logger.info("VM connect info stored in file '{}'".format(vm_info_file_name))

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)
    
    
    
    
@login_required
def iaas_list(request):

    wizardboxes_fields = dict()

# FIXME - set obj as string
    
    wizardboxes_fields = get_apidata("wizardboxes", request)

    # for api in ['providers',]:
    #   wizardboxes_fields[api] = Provider.objects.all().values() #get_apidata(api)


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields})

    CONTEXT.update({ 'request': request, })

    # pprint(CONTEXT, indent=4)
    _logger.info("{} LIST".format(API_NAME), CONTEXT)
    return render(request, 'frontend/includes/%s/list.html' % API_NAME, CONTEXT)


# @cache_page(DEFAULT_CACHE_TIME)
@login_required
def iaas_wizardbox_create(request):
    wizardboxes_fields = get_apidata("wizardboxes", request)
    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })
    CONTEXT.update({'request': request, })

    projects = get_apidata('projects', request)
    projects = projects.get('results') or []
    api = dict(
        providers       = get_apidata('providers', request),
        projects        = projects,
        usercredentials = get_apidata('usercredentials', request),
        usersecrets     = get_apidata('usersecrets', request),
        imagegroups     = get_apidata('provisioning/iaac/image_groups/list', request),
        plangroups      = get_apidata('provisioning/iaac/plan_groups/list', request),
        storages        = get_apidata('provisioning/iaac/storage/amazon_ec2/list', request)
    )

    CONTEXT.update({'api': api})

    return render(request, 'frontend/includes/%s/wizardbox_create.html' % API_NAME, CONTEXT)


def iaas_create(request):
    if request.method == 'POST':
        form = ahomeForm(request.POST)
    else:
        form = ahomeForm()

    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


def iaas_update(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)



def iaas_delete(request, pk):


    instance = get_object_or_404(MODEL_OBJ, pk=pk)
    
    data = dict()
    
    if request.method == 'POST':
        
        instance.delete()

        data['form_is_valid'] = True  # This is just to play along with the existing code

        apidata = get_apidata(API_NAME, request)

        CONTEXT.update({ 'apidata': apidata, 'ops': 'delete', })
        
        data['html_model_list'] = render_to_string('frontend/includes/%s/list.html' % API_NAME, CONTEXT)
        
        data['html_toast_notification'] = render_to_string('frontend/includes/helpers/alert-success.html', CONTEXT)

        data['html_search_nav'] = render_to_string('frontend/includes/helpers/search.html', CONTEXT)

    else:
  
        CONTEXT.update({ 'instance': instance, })
        data['html_form'] = render_to_string('frontend/includes/%s/delete.html' % API_NAME,
            CONTEXT,
            request=request,
        )
    return JsonResponse(data)







