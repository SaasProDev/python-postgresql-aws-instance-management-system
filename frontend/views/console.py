
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




API_NAME = 'console'
MODEL_NAME = 'Provider'
MODEL_OBJ = Provider


URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
CONTEXT = { 'api_name': API_NAME, 'model_name': MODEL_NAME, 'include_path': INCLUDE_PATH, 'url_create': URL_CREATE, 'url_update': URL_UPDATE, 'url_delete': URL_DELETE }


def console(request):

    # apidata = get_apidata(API_NAME, request)

    # CONTEXT.update({ 'apidata': apidata, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)




# def console_create(request):


#     if request.method == 'POST':
#         form = ahomeForm(request.POST)
#     else:
#         form = ahomeForm()

#     return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


# def console_update(request, pk):
    

#     instance = get_object_or_404(MODEL_OBJ, pk=pk)

#     if request.method == 'POST':
#         form = ahomeForm(request.POST, instance=instance)
#     else:
#         form = ahomeForm(instance=instance)
#     return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)











