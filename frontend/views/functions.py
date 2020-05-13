from django.template.loader import render_to_string
from django.utils.translation import gettext as _
import requests
from django.conf import settings
import ast

from django.http import *
from django.shortcuts import redirect
from django.template import RequestContext

import os
import pprint
from django.apps import apps

from logging import getLogger

_logger = getLogger(__name__)

# def index(request):
#     return render(request, 'frontend/main.html')


# def my_django_view(request):
#     if request.method == 'POST':
#         r = requests.post('https://www.somedomain.com/some/url/save', params=request.POST)
#     else:
#         r = requests.get('https://www.somedomain.com/some/url/save', params=request.GET)
#     if r.status_code == 200:
#         return HttpResponse('Yay, it worked')
#     return HttpResponse('Could not save data')

OPS = dict()

OPS['create'] = _("created")
OPS['update'] = _("updated")
OPS['delete'] = _("deleted")

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join('/ahome_devel/','ssl/rootCA.pem')

# os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
#     '/etc/ssl/certs/',
#     'ca-certificates.crt')


def get_apidata(model_name, request):
    headers = dict()

    if "token__refresh" in request.session:
        request.session['token__access'] = refresh_token(request.session['token__refresh'])
        headers = { "content-type": "application/json", "Authorization": "Bearer {}".format(request.session['token__access']) }
    else:
        #redirect("login")
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            headers = {"content-type": "application/json",
                       "Authorization": authorization_header}

    url = '{}/{}/{}/'.format(settings.AHOME_INTERNAL_API, settings.AHOME_INTERNAL_API_VERSION, model_name)

    if model_name not in ['wizardboxes']:
        if request.GET:
            url = "{}?{}".format(url, request.GET.urlencode() )

    _logger.debug("Frontend Page loading...  '{}' headers: {}".format(url, headers))
    response = requests.get(url, headers=headers)

    try:
        apidata = response.json()
    except Exception as ex:
        _logger.error("Cannot load Frontend Page '{}'; Exception: {}".format(url, ex))
        return None
    else:
        return apidata


def get_detail_apidata(model_name, pk, request):
        # obj = model_name
    app_name = 'core'
    # obj = apps.get_model(app_label=app_name, model_name=model_name)
    # i = Invoice.objects.filter(id=1234).first()
    # return obj.objects.all()
    headers = dict()

    if "token__refresh" in request.session:
        request.session['token__access'] = refresh_token(request.session['token__refresh'])
        headers={ "content-type": "application/json", "Authorization": "Bearer {}".format(request.session['token__access']) }
    else:
        redirect("login")


    # url = 'http://127.0.0.1:8001/api/v1/%s/' % model_name
    url = '{}/{}/{}/{}/'.format(settings.AHOME_INTERNAL_API, settings.AHOME_INTERNAL_API_VERSION, model_name, pk )

    if model_name not in ['wizardboxes']:

        if request.GET:
            url = "{}?{}id={}".format(url, request.GET.urlencode(), pk )

    # print (url)

    response = requests.get(url, headers=headers)
    try:
        apidata = response.json()
    except Exception as ex:
        print("ERROR")
        return None
    else:
        return apidata



def post_apidata(model_name, request):
    # obj = model_name
    app_name = 'core'

    url = '{}/{}/'.format(settings.AHOME_INTERNAL_API, model_name )

    apidata = dict()

    if request.POST:
        data = request.POST #json.loads(request.POST)
        response = requests.post( url, data=data )
        apidata = response.json()

    # print (apidata)

    return apidata


def refresh_token(token_refresh):
    # obj = model_name
    app_name = 'core'

    url = '{}/token/refresh/'.format( settings.AHOME_INTERNAL_API )

    # apidata = dict()
    data = dict( refresh = token_refresh )
    response = requests.post( url, data=data )
    apidata = response.json()

    return apidata.get('access', {})



def save_form(request, form, template_name, ops, api_name, model_name, context=None, app_name='core'):
    """ Universal Form for ALL Models"""

    context = context or {}
    data = dict()

    user = request.user
    model = apps.get_model("{}.{}".format(app_name, model_name))

    _logger.debug("Applying '{}' form for user: '{}'...".format(api_name, user))

    snippet_html = 'frontend/includes/%s/list.html' % api_name

    if request.method == 'POST':
        form_data = form.data

        print("*** INPUT FORM ***")
        pprint.pprint(form_data)

        if form.is_valid():
            obj = form.save(commit=False)
            if form_data.get('credential-kind') and form_data.get('credential-schema'):
                schema = ast.literal_eval(form_data['credential-schema'])
                obj.schema = schema
                obj.kind = form_data['credential-kind']
                initial = dict()
                for c in ast.literal_eval(form_data['credential-schema']):
                    field = "credential-{}".format(c.get('name'))
                    initial[c.get('name')] = form_data[field]
                obj.inputs = initial

            if hasattr(model, 'owner'):
                obj.owner = user

            if hasattr(model, 'pre_create'):
                obj.pre_create(user, form_data=form_data)

            obj.save()

            if hasattr(model, 'post_create'):
                obj.post_create(user, form_data=form_data)
                obj.save()

            data['form_is_valid'] = True

            # organizations = Organization.objects.all()
            apidata = get_apidata(api_name, request)

            context.update({'apidata': apidata, 'model_name': model_name, 'api_name': api_name, 'ops': OPS[ops]})

            data['html_model_list'] = render_to_string(snippet_html, context)
            data['html_toast_notification'] = render_to_string('frontend/includes/helpers/alert-success.html', context )
            data['html_search_nav'] = render_to_string('frontend/includes/helpers/search.html', context )
        else:
            data['form_is_valid'] = False

    context.update({'form': form, 'model_name': model_name, 'api_name': api_name})

    data['html_form'] = render_to_string(template_name, context, request=request)

    # from django.core import django_serializers
    # raw = django_serializers.serialize("json", request)

    return JsonResponse(data)