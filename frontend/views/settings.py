
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



from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect




# from frontend.forms import GenerateRandomVirtualMachineForm
# from core.tasks import create_random_virtual_machines




# class GenerateRandomVirtualMachinesView(FormView):
#     template_name = 'frontend/trash/demo.html'
#     form_class = GenerateRandomVirtualMachineForm
#     success_url = '/tasks'


#     def form_valid(self, form):
#         total = form.cleaned_data.get('total')
#         create_random_virtual_machines.delay(total)
#         messages.success(self.request, 'We are generating your random virtual machines! Wait a moment and refresh this page.')
#         return redirect('demo-tasks')





# class GenerateRandomUserView(FormView):
#     template_name = 'core/generate_random_users.html'
#     form_class = GenerateRandomUserForm

#     def form_valid(self, form):
#         total = form.cleaned_data.get('total')
#         create_random_user_accounts.delay(total)
#         messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
#         return redirect('users_list')


# CONTEXT.update({ "{}_active".format(API_NAME): 'active', })

def settings(request):
    context = { "{}_active".format('settings'): 'active', }
    return render(request, 'frontend/src/settings.html', context)

