
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

from .functions import OPS, get_apidata, post_apidata, save_form

from frontend.forms import ProviderForm as ahomeForm


from frontend.forms import get_form as ahomeWizardForm

# from .database_dict import DICT_CREDENTIALS

from core.utils import DICT_CREDENTIALS

import os



from django.http import *
from django.shortcuts import redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

import logging
logger = logging.getLogger(__name__)

API_NAME = 'token'

MODEL_NAME = 'Token'
# MODEL_OBJ = User


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
 
    )


CONTEXT.update({ "{}_active".format(API_NAME): 'active', })

def token_logout(request):

    logout(request)
    try:
        del request.session['token__refresh']
        del request.session['token__access']

    except Exception as e:
        pass
    # messages.info(request, "Logged out successfully!")
    return redirect("login")

    
    

    # return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)



def token_login(request):

    # logout(request)
    form = AuthenticationForm()
    CONTEXT.update({ "form":{'errors' : ''} })

    username = password = ''

    if request.POST:

        if request.POST.get('username') and request.POST.get('password'):
            
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            logger.error("*** apidata {}".format(user))
            if user is not None:
                
                if user.is_active:
                    
                    login(request, user)

                    apidata = post_apidata(API_NAME, request)
                    CONTEXT.update({ 'apidata': apidata, })

                    request.session['token__refresh'] = apidata.get('refresh')
                    request.session['token__access'] = apidata.get('access')

                    # print("*** apidata {}".format(apidata))
                    # print("*** sessions {}".format(request.session))

                    logger.error("*** apidata {}".format(apidata))
                    logger.error("*** sessions {}".format(request.session))
                    
                    # return HttpResponseRedirect('/')
                    return redirect("index")
            else:
                CONTEXT.update({ "form":{'errors' : 'true'} })
        else:
            return redirect("index")
                    

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)
