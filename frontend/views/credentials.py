
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _

import requests

from core.models import *

from frontend.forms import *

from django.apps import apps

from .functions import OPS, get_apidata, save_form

from frontend.forms import CredentialForm as ahomeForm




# from frontend.forms import CustomForm as ahomeForm
# from frontend.forms import CustomForm as ahomeJsonForm

# from django_jsonforms.forms import JSONSchemaForm

# formJson = JSONSchemaForm(schema=first_name_schema , options=options , ajax=False)


from frontend.forms import get_form as ahomeWizardForm


# json_form = get_json_form_from_somewhere()
# wizardform = ahomeWizardForm(jsonform)

# from .database_dict import DICT_CREDENTIALS

from core.utils import DICT_CREDENTIALS



# credentials_json = dict(
#   generic = [{
#       "name": "inventory",
#       "label": "Hostname or IP",
#       "type": "text",
#       "required": 1,
#       "help_text": "Enter remote IP or Hostname"
#   },
#   {
#       "name": "username",
#       "label": "Username",
#       "type": "text",
#       "required": 1,
#       "help_text": "Enter your Username"
#   },

#   {
#       "name": "password",
#       "label": "Password",
#       "type": "password",
#       "required": 1,
#       "help_text": "Enter your SSH Password"
#   },

#   ],

#   kvm = [{
#       "name": "inventory",
#       "label": "Hostname or IP",
#       "type": "text",
#       "required": 1,
#       "help_text": "Enter remote IP or Hostname"
#   },
#   {
#       "name": "username",
#       "label": "Username",
#       "type": "text",
#       "required": 1,
#       "help_text": "Enter your Username"
#   },
#   {
#       "name": "password",
#       "label": "Password",
#       "type": "password",
#       "required": 1,
#       "help_text": "Enter your SSH Password"
#   },


#   ],

#   appliance = [{
#       "name": "inventory",
#       "label": "Hostname or IP",
#       "type": "text",
#       "required": 1,
#       "help_text": "Enter remote IP or Hostname"
#   },
#   {
#       "name": "username",
#       "label": "Appliance Username",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "Enter appliance Username"
#   },
#   {
#       "name": "password",
#       "label": "Appliance Password",
#       "type": "password",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "Enter Appliance Password"
#   },

#   ],

#   amazon_ec2 = [{
#       "name": "AWS_ACCESS_KEY_ID",
#       "label": "AWS ACCESS KEY ID",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "Enter AWS Access Key ID"
#   },
#   {
#       "name": "AWS_SECRET_ACCESS_KEY",
#       "label": "AWS SECRET ACCESS KEY",
#       "type": "password",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "Enter AWS Access Key"
#   },
#   {
#       "name": "AWS_SECURITY_TOKEN",
#       "label": "AWS SECURITY TOKEN",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "Enter AWS Security Token"
#   },

#   ],

#   azure_rm = [{
#       "name": "AZURE_SUBSCRIPTION_ID",
#       "label": "AZURE SUBSCRIPTION ID",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "AZURE SUBSCRIPTION ID"
#   },
#   {
#       "name": "AZURE_CLIENT_ID",
#       "label": "AZURE CLIENT ID",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "AZURE CLIENT ID"
#   },
#   {
#       "name": "AZURE_TENANT",
#       "label": "AZURE TENANT",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "AZURE TENANT"
#   },

#   {
#       "name": "AZURE_SECRET",
#       "label": "AZURE SECRET",
#       "type": "password",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "AZURE SECRET"
#   },

#   {
#       "name": "AZURE_AD_USER",
#       "label": "AZURE AD USER",
#       "type": "text",
#       "max_length": 25,
#       "required": 0,
#       "help_text": "AZURE TENANT"
#   },

#   {
#       "name": "AZURE_PASSWORD",
#       "label": "AZURE PASSWORD",
#       "type": "password",
#       "max_length": 25,
#       "required": 0,
#       "help_text": "AZURE PASSWORD"
#   },

#   {
#       "name": "AZURE_CLOUD_ENVIRONMENT",
#       "label": "AZURE CLOUD ENVIRONMENT",
#       "type": "password",
#       "max_length": 25,
#       "required": 0,
#       "help_text": "AZURE CLOUD ENVIRONMENT"
#   },


#   ],

#   vmware = [{
#       "name": "VMWARE_HOST",
#       "label": "VMWARE HOST",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "VMWARE HOST"
#   },
#   {
#       "name": "VMWARE_USER",
#       "label": "VMWARE USER",
#       "type": "text",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "VMWARE USER"
#   },
#   {
#       "name": "VMWARE_PASSWORD",
#       "label": "VMWARE PASSWORD",
#       "type": "password",
#       "max_length": 25,
#       "required": 1,
#       "help_text": "VMWARE PASSWORD"
#   },
#   {
#       "name": "VMWARE_VALIDATE_CERTS",
#       "label": "VMWARE VALIDATE CERTS",
#       "type": "checkbox",
#       "required": 1,
#       "help_text": "VMWARE VALIDATE CERTS"
#   },

#   ],



# )


credentials_json = DICT_CREDENTIALS



API_NAME = 'credentials'
MODEL_NAME = 'Credential'
MODEL_OBJ = Credential


URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
# CONTEXT = { 'api_name': API_NAME, 'model_name': MODEL_NAME, 'include_path': INCLUDE_PATH, 'url_create': URL_CREATE, 'url_update': URL_UPDATE, 'url_delete': URL_DELETE, 'credentialform': WizardForm(prefix='credential', jsonform=libvirtform, initial={'username': 'userec2', 'password': 'secret_password'}), }

jsonform = credentials_json.get("generic")

CONTEXT = dict(
    api_name = API_NAME, 
    model_name = MODEL_NAME, 
    include_path = INCLUDE_PATH, 
    url_create = URL_CREATE,
    url_update = URL_UPDATE,
    url_delete = URL_DELETE,
    credentialform = WizardForm(prefix='credential', jsonform=jsonform, initial={}),

    )


def credentials_form(request, kind):


    # apidata = get_apidata(API_NAME, request)
    # CONTEXT.update({ 'apidata': apidata, })


    defaultform = credentials_json.get("generic")

    jsonform = credentials_json.get(kind, defaultform)

    hiddeninputs = dict(
        kind = kind,
        schema = jsonform,
        )


    # jsonform.append( 
    #   {
    #       "name": "credential-kind",
    #       "type": "text",
    #       "default": kind
    #   }
    #   )

    # initial = {'username': 'user-wee', 'password': 'secret-password'}

    initial = {}
    CONTEXT.update({ 'credentialform': WizardForm(prefix='credential', jsonform=jsonform, initial=initial), 'hiddeninputs': hiddeninputs })

    data = dict()
    data['html_form'] = render_to_string('frontend/includes/helpers/credentialform.html', CONTEXT)
    data['data'] = jsonform

    return JsonResponse(data)





def credentials(request):


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)


def credentials_list(request):


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, })

    return render(request, 'frontend/includes/%s/list.html' % API_NAME, CONTEXT)



def credentials_create(request):


    if request.method == 'POST':
        form = ahomeForm(request.POST)
    else:
        form = ahomeForm()

    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


def credentials_update(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)



def credentials_delete(request, pk):


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





