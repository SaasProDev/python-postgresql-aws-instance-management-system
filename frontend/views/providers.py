
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

from frontend.forms import ProviderForm as ahomeForm




# from frontend.forms import CustomForm as ahomeForm
# from frontend.forms import CustomForm as ahomeJsonForm

# from django_jsonforms.forms import JSONSchemaForm

# formJson = JSONSchemaForm(schema=first_name_schema , options=options , ajax=False)


from frontend.forms import get_form as ahomeWizardForm

# from .database_dict import DICT_CREDENTIALS

from core.utils import DICT_CREDENTIALS

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






API_NAME = 'providers'
MODEL_NAME = 'Provider'
MODEL_OBJ = Provider


CREDENTIAL_JSON = 'credential_form'
URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
URL_CREDENTIAL = '%s_credential' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
CONTEXT = dict(
    api_name = API_NAME,
    model_name = MODEL_NAME, 
    include_path =  INCLUDE_PATH, 
    url_create = URL_CREATE, 
    url_update = URL_UPDATE,
    url_delete = URL_DELETE,
    url_credential = URL_CREDENTIAL,
    credential_json = CREDENTIAL_JSON,
    # wizardform = WizardForm(prefix='wizard', jsonform=jsonform, initial={'firstname': 'Afahounko', 'lastname': 'Danny', 'age': 37, 'occupation': 'engineer'}),
    # credentialform = WizardForm(prefix='crendential', jsonform=libvirtform, initial={'username': 'userec2', 'password': 'secret_password'}),

    )


CONTEXT.update({ "{}_active".format(API_NAME): 'active', })


def providers(request):

    wizardboxes_fields = dict()
    wizardboxes_fields = get_apidata("wizardboxes", request)

    apidata = get_apidata(API_NAME, request)

    # CONTEXT.update({ 'apidata': apidata, })
    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)

def providers_list(request):

    wizardboxes_fields = dict()
    wizardboxes_fields = get_apidata("wizardboxes", request)

    apidata = get_apidata(API_NAME, request)

    # CONTEXT.update({ 'apidata': apidata, })
    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })

    return render(request, 'frontend/includes/%s/list.html' % API_NAME, CONTEXT)


def providers_create(request):

    # jsonform = DICT_CREDENTIALS.get("kvm")

    kind = "kvm"
    jsonform = DICT_CREDENTIALS.get(kind)

    hiddeninputs = dict(
        kind = kind,
        schema = jsonform,
        )



    CONTEXT.update(dict(
        credentialform = WizardForm(prefix='credential', jsonform=jsonform, initial={}),
        hiddeninputs = hiddeninputs,
        ))

    if request.method == 'POST':
        form = ahomeForm(request.POST)
    else:
        form = ahomeForm()

    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


def providers_update(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)




def providers_credential(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    jsonform = instance.schema

    initial = instance.inputs

    hiddeninputs = dict(
        kind = instance.kind,
        schema = instance.schema,
        )

    CONTEXT.update(dict(
        credentialform = WizardForm(prefix='credential', jsonform=jsonform, initial=initial),
        hiddeninputs = hiddeninputs,
        ))

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/credential.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)





def providers_delete(request, pk):


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





