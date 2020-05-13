import copy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _

import requests

from core.models import *

from frontend.forms import *

from django.apps import apps

from .functions import OPS, get_apidata, save_form

from frontend.forms import UserForm as ahomeForm

from logging import getLogger

_logger = getLogger(__name__)


APP_NAME = 'account'
API_NAME = 'users'
MODEL_NAME = 'User'
MODEL_OBJ = User


URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
CONTEXT = { 'api_name': API_NAME, 'model_name': MODEL_NAME, 'include_path': INCLUDE_PATH, 'url_create': URL_CREATE, 'url_update': URL_UPDATE, 'url_delete': URL_DELETE,  }

CONTEXT.update({ "{}_active".format(API_NAME): 'active', })

def users(request):


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)


def users_list(request):
    apidata = get_apidata(API_NAME, request)
    CONTEXT.update({ 'apidata': apidata, })
    return render(request, 'frontend/includes/%s/list.html' % API_NAME, CONTEXT)


@login_required
def users_create(request):
    from account.models import Organization
    user = request.user
    query_set = user.get_available_objects(Organization, mode='grant')
    organizations = [{'name': o.name, 'uuid': o.uuid} for o in query_set.all()]
    form = ahomeForm(request.POST) if request.method == 'POST' else ahomeForm()
    context = copy.deepcopy(CONTEXT)
    context['extra'] = {'organizations': organizations}
    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, context, APP_NAME)


def users_update(request, pk):
    instance = get_object_or_404(MODEL_OBJ, pk=pk)
    form = ahomeForm(request.POST, instance=instance) if request.method == 'POST' else ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT, APP_NAME)


def users_delete(request, pk):
    _logger.warning("USER CANNOT BE DELETED. is_active = False for Now")

    instance = get_object_or_404(MODEL_OBJ, pk=pk)
    instance.is_active = False
    return JsonResponse({"status": "SKIPPED"})

    #
    #
    # data = dict()
    #
    # if request.method == 'POST':
    #
    #     instance.delete()
    #     data['form_is_valid'] = True  # This is just to play along with the existing code
    #
    #     apidata = get_apidata(API_NAME, request)
    #
    #     CONTEXT.update({ 'apidata': apidata, 'ops': 'delete', })
    #     data['html_model_list'] = render_to_string('frontend/includes/%s/list.html' % API_NAME, CONTEXT)
    #     data['html_toast_notification'] = render_to_string('frontend/includes/helpers/alert-success.html', CONTEXT)
    #     data['html_search_nav'] = render_to_string('frontend/includes/helpers/search.html', CONTEXT)
    #
    # else:
    #
    #     CONTEXT.update({ 'instance': instance, })
    #     data['html_form'] = render_to_string('frontend/includes/%s/delete.html' % API_NAME,
    #         CONTEXT,
    #         request=request,
    #     )
    # return JsonResponse(data)







