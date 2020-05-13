import traceback
from pprint import pformat
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _
# from django.conf import settings



import requests

from core.models import *
# from core.models import Project

from frontend.forms import *

from django.apps import apps

from .functions import OPS, get_apidata, save_form

from frontend.forms import WizardBoxForm as ahomeForm

from django.conf import settings as django_settings

import yaml
import json
import ast
from collections import OrderedDict

from logging import getLogger

# from frontend.forms import CustomForm as ahomeForm
# from frontend.forms import CustomForm as ahomeJsonForm

# from django_jsonforms.forms import JSONSchemaForm

# formJson = JSONSchemaForm(schema=first_name_schema , options=options , ajax=False)


from frontend.forms import get_form as ahomeWizardForm


# json_form = get_json_form_from_somewhere()
# wizardform = ahomeWizardForm(jsonform)

# from .database_dict import DICT_CREDENTIALS, DICT_WIZARDBOXFORMS

from core.utils import DICT_CREDENTIALS, DICT_WIZARDBOXFORMS
# from core.utils import DICT_CREDENTIALS
from core.utils import load_yml_to_dict, ahomefile_to_dict, dict_yaql, append_ahomefile_fields, ahomefile_yaql

wizardboxes_json = DICT_WIZARDBOXFORMS


#TODO: Move to settings
# AHOMEFILES_PATH = "/ahome_devel/ahomefiles"

_logger = getLogger(__name__)

DEFAULT_CACHE_TIME = django_settings.DEFAULT_CACHE_TIME


API_NAME = 'wizardboxes'
MODEL_NAME = 'WizardBox'
MODEL_OBJ = WizardBox


URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
# CONTEXT = { 'api_name': API_NAME, 'model_name': MODEL_NAME, 'include_path': INCLUDE_PATH, 'url_create': URL_CREATE, 'url_update': URL_UPDATE, 'url_delete': URL_DELETE, 'wizardboxform': WizardForm(prefix='wizardbox', jsonform=libvirtform, initial={'username': 'userec2', 'password': 'secret_password'}), }

jsonform = wizardboxes_json.get("default")

CONTEXT = dict(
	api_name = API_NAME, 
	model_name = MODEL_NAME,
	include_path = INCLUDE_PATH, 
	url_create = URL_CREATE,
	url_update = URL_UPDATE,
	url_delete = URL_DELETE,
	wizardboxform = WizardForm(prefix='wizardbox', jsonform=jsonform, initial={}),

	)



def mk_int(s, default=0):
    try:
        return int(s.strip())
    except:
        _logger.warning("Cannot get value '{}' as integer. SKIPPED. Applied default={}".format(s, default))
        return default


def generateform(kind):
    data = dict()
    output = OrderedDict()


    # ahomefile = "{}/{}.yml".format(AHOMEFILES_PATH, kind)
    # try:
    #     data = yaml.load(open(ahomefile), Loader=yaml.SafeLoader)
    # except Exception as e:
    #     raise e
    #     # pass
    # # print(ahomefile)
    # # print(data)

    data = ahomefile_to_dict(kind)

    output["name"] = data.get("name")
    output["description"] = data.get("description")
    output["title"] = data.get("title")
    output["cloud"] = data.get("cloud", False)
    output["success_msg"] = data.get("success_msg", _("Deployment completed with success"))



    for item in ['fields', 'credentials']:
        output[item] = []
        output["{}_advanced".format(item)] = []

        f = data.get(item, dict())
        for field in f:

            if not field.get("type"):
                field.update(dict( type = "text"))

            if not field.get("label"):
                field.update( dict( label = field.get("name") ) )


            if field.get("advanced"):
                output["{}_advanced".format(item)].append(field)
            else:
                output[item].append(field)


    return output



def render_jsonform( request, kind, schemafields, schemafields_advanced, schemacredentials, schemacredentials_advanced, initial=dict(), instance=dict(), credentialsfield=dict()  ):
    
    output = dict()

    ahomefile = generateform(kind)

    hiddeninputs = dict(
        kind = kind,
        schemafields = schemafields,
        schemafields_advanced = schemafields_advanced,
        schemacredentials = schemacredentials,
        schemacredentials_advanced = schemacredentials_advanced,
        # ahomefile = ahomefile,
        credentialsfield = credentialsfield,
        )

    CONTEXT.update( dict(
        wizardboxform = WizardForm(prefix='wizardbox', jsonform=schemafields, initial=initial),
        wizardboxform_advanced = WizardForm(prefix='wizardbox', jsonform=schemafields_advanced, initial=initial),
        credentialboxform = WizardForm(prefix='wizardbox', jsonform=schemacredentials, initial=initial),
        credentialboxform_advanced = WizardForm(prefix='wizardbox', jsonform=schemacredentials_advanced, initial=initial),
        hiddeninputs = hiddeninputs,
        ahomefile = ahomefile,
        instance = instance,
        )
    )



    CONTEXT.update( dict( api = dict(
        providers = get_apidata('providers', request),
        usercredentials = get_apidata('usercredentials', request),
        usersecrets = get_apidata('usersecrets', request),
                                ) 
                        )
                    )

    output['html_form'] = render_to_string('frontend/includes/helpers/wizard-modal-content.html', CONTEXT)
    

    return output



def wizardboxesform_generate(request, kind, model, pk):


    # apidata = get_apidata(API_NAME, request)
    # CONTEXT.update({ 'apidata': apidata, })

    defaultform = wizardboxes_json.get("default")

    ahomefile = generateform(kind)

    schemafields = ahomefile.get("fields")
    schemafields_advanced = ahomefile.get("fields_advanced")
    schemacredentials = DICT_CREDENTIALS.get('secret') #ahomefile.get("credentials")
    schemacredentials_advanced = DICT_CREDENTIALS.get('sshkey') #ahomefile.get("credentials_advanced")

    initial = dict()
    instance=dict()
    credentialsfield = dict()

    if model and pk:
        credentialsfield[model] = pk

    data = render_jsonform(request, kind, schemafields, schemafields_advanced, schemacredentials, schemacredentials_advanced, initial, instance, credentialsfield)

    return JsonResponse(data)



def wizardboxesform_provider(request, kind, model):


    # apidata = get_apidata(API_NAME, request)
    # CONTEXT.update({ 'apidata': apidata, })

    defaultform = wizardboxes_json.get("default")

    ahomefile = generateform(kind)

    schemafields = ahomefile.get("fields")
    schemafields_advanced = ahomefile.get("fields_advanced")
    schemacredentials = DICT_CREDENTIALS.get('secret') #ahomefile.get("credentials")
    schemacredentials_advanced = DICT_CREDENTIALS.get('sshkey') #ahomefile.get("credentials_advanced")

    initial = dict()
    instance=dict()
    credentialsfield = dict()

    # if model and pk:
    #     credentialsfield[model] = pk

    data = render_jsonform(request, kind, schemafields, schemafields_advanced, schemacredentials, schemacredentials_advanced, initial, instance, credentialsfield)

    return JsonResponse(data)


@csrf_exempt
def wizardboxesform_save(request, model, kind):
    """
    Create / Update  'IaaS'
    add 'UserCredential' if ones was not set up before
    """
    data = dict()
    schema_hiddenlist = ['fields', 'fields_advanced', 'credentials', 'credentials_advanced']

    if request.method == 'POST':
        data = dict(request.POST.lists())
        _logger.debug("Input data: {}".format(pformat(data, indent=4)))

        kind        = request.POST.get('ahome_kind')
        fields      = request.POST.get('ahome_fields')
        credentials = request.POST.get('ahome_credentials')

        if not (kind and fields and credentials):
            _logger.error("Important fields are missing. Entered data: {}".format(request.POST))
            raise Exception("Important fields are missing")
        else:
            iaas_name = request.POST.get('ahome_name', None)
            instance_id = mk_int(request.POST.get('ahome_instance_id'))
            f__credentialsfield = ast.literal_eval(request.POST.get('ahome_credentialsfield'))

            f__inputs = dict()
            f__schema = dict()
            current_processed = None
            try:
                for section in schema_hiddenlist:
                    try:
                        hidden_field = ast.literal_eval(request.POST.get("ahome_{}".format(section) ))
                    except:
                        _logger.warning("Set of parameters are not presented: '{}'. SKIPPED".format(section))
                        continue

                    f__schema[section] = hidden_field

                    for field in hidden_field:
                        current_processed = field

                        field_type = field.get('type')
                        field_name = field.get('name')

                        extended_field_name = "wizardbox-{}".format(field_name)
                        extended_field_value = request.POST.get(extended_field_name)

                        if request.POST.get(extended_field_name):
                            _logger.debug("processing '{}'..".format(extended_field_name))
                            if field_type == 'checkbox':
                                f__inputs[field_name] = bool(extended_field_value)
                            elif field_type == 'integer':
                                f__inputs[field_name] = mk_int(extended_field_value)
                            else:
                                f__inputs[field_name] = extended_field_value
                        else:
                            _logger.warning("Extra field during form processing: "
                                            "name:'{}' type:'{}'".format(field_name, field_type))
                            # save as false if key does not exist or not submitted
                            if field_type == 'checkbox':
                                f__inputs[field_name] = bool('')
                        # else:
                        #     f__inputs[f.get('name')] = None


            except Exception as ex:
                _logger.error("Cannot process input value. {}.. {}; SKIPPED".format(
                    ex, traceback.format_exc(), current_processed))

            _logger.debug("Form INPUTS: {}".format(pformat(f__inputs, indent=4)))

            # f_ahomefile = ast.literal_eval(request.POST.get('ahome_ahomefile'))

            if instance_id == 0:
                credential_id = f__credentialsfield.get('usercredential')

                if not credential_id:
                    _logger.error("IaaS credentials does not defined.")
                    raise Exception("Cannot create IaaS instance because no credentials")
                try:
                    usercredential = UserCredential.objects.get(id=credential_id)
                    obj = IaaS.objects.create(
                        name=iaas_name,
                        inputs=f__inputs,
                        schema=f__schema,
                        kind=kind,
                        credentials=f__credentialsfield,
                        usercredential=usercredential,
                        )
                    obj.save()
                    _logger.debug("New IaaS instance CREATED. Name: '{}' Inputs:{}".format(iaas_name, f__inputs))
                except Exception as ex:
                    _logger.error("Cannot create IaaS instance. "
                                  "Name={}; Inputs:{}; Exception: {}".format(iaas_name, f__inputs, ex))
                    raise Exception("Cannot create IaaS instance")
            else:
                try:
                    IaaS.objects.filter(id=instance_id).update(
                        name=iaas_name,
                        inputs=f__inputs)
                    _logger.debug("IaaS instance updated. "
                                  "Id={}; Inputs:{}".format(instance_id, f__inputs))
                except Exception as ex:
                    _logger.error("Cannot update IaaS instance. "
                                  "Id={}; Inputs:{}; Exception: {}".format(instance_id, f__inputs, ex))

                    raise Exception("Cannot update IaaS instance")

    return JsonResponse(data)



"""
IaaS cretate Data Example

{   'f-modal-authentication-key': ['TEST DUMMY SSH'],
    'f-modal-authentication-secret': ['hello@world.com'],
    'f-modal-costs': ['16.94'],
    'f-modal-count': ['2'],
    'f-modal-image': [   "{'image_id': 1, 'name': 'Ubuntu', 'label': 'Ubuntu', "
                         "'iconClass': 'ahome/assets/ubuntu-icon.svg', "
                         "'default': '18.04 LTS', 'version': ['18.04 LTS', "
                         "'16.04 LTS', '14.04 LTS'], 'group_id': 1}"],
    'f-modal-image-version': ['18.04 LTS'],
    'f-modal-instance': [''],
    'f-modal-name': ['ddd'],
    'f-modal-plan': [   "{'plan_id': 1, 'name': '1vcpu_1gb_10gb', 'price': "
                        "0.0116, 'rate': 'hour', 'vcpu': 1, 'memory': 1, "
                        "'disk': 10, 'traffic': 'unlimited traffic', "
                        "'currency': 'dollar'}"],
    'f-modal-project': ['Default Project'],
    'f-modal-provider': ['2'],
    'f-modal-provider-kind': ['amazon_ec2'],
    'f-modal-provider-name': ['Sergii Real'],
    'f-modal-storage': ['{}'],
    'f-modal-tags': ['']}

"""


def param_value(request, param_name, default=None):
    return request.POST.get(param_name, default)


def get_or_create_project(request, user, project_name, iaas_name=None):

    # -- NO PROJECT CREATION DURING THE IAAS create - if no project available then User creation process is wrong
    # TODO - Create method to have default ORG, Default Project


    # projects = list(Project.objects.filter(name=project_name).all())
    # projects = user.get_available_objects(Project, mode='read').filter(name=project_name).all()


    projects = get_apidata("projects", request)

    if projects.get('count', 0) > 0:
        project = projects.results[0]   # todo CHECK Ownership
    else:
        project = None
        project_name = project_name or "Auto for {}".format(user)

    if not project:
        organization = user.get_default_organization()
        project = Project.create(organization, user,
                                         name=project_name,
                                         description="For '{}' auto created".format(iaas_name))

        _logger.debug("Auto create Project '{}' for IaaS '{}'".format(project_name, iaas_name))
    return project

#TODO: FIX-ME
@csrf_exempt
def wizardGenericform_save(request):
    user = request.user
    data = dict( )
    schema_hiddenlist = ['fields', 'fields_advanced', 'credentials', 'credentials_advanced']

    if request.method == 'POST':

        data = dict(request.POST.lists())

        _logger.debug("Data:\n{}".format(pformat(data, indent=4)))
        # _logger.info("Data-f-modal-image: '{}'".format(data.get('f-modal-image')))

        applications = []
        # try:
        image_name = request.POST.get('f-modal-image')
        f_modal_image = ast.literal_eval(image_name)
        applications = f_modal_image.get('apps', [])

        # except:
        #     _logger.error("No good Image defined for start [{}]. ACTION CANCELLED".format(request.POST.get('f-modal-image')))
        #     JsonResponse({"status": "ERROR"})

        iaas_name = request.POST.get('f-modal-name')

        x = request.POST.get('f-modal-image')
        f_modal_image = ast.literal_eval(x)

        x = request.POST.get('f-modal-plan')
        f_modal_plan = ast.literal_eval(x)


        # project = get_or_create_project(user, f_modal_project, iaas_name)
        # PROJECT

        x = request.POST.get('f-modal-project')
        f_modal_project_uuid = str(x)

        if f_modal_project_uuid:
            project = Project.objects.get(uuid = f_modal_project_uuid)
        else:
            # GET DEFAULT PROJECT
            output = get_apidata("projects", request)
            if output.get('count') > 0:
                project_uuid = output.get('results')[0]
                project = Project.objects.get( uuid = project_uuid.get('uuid') )
            else:
                _logger.warning("No available Project, Please Create one")
                raise "NO PROJECT AVAILABLE FOR THIS USER"

        # END PROJECT

        # apps = [n.strip() for n in x]
        usercredential_id = request.POST.get('f-modal-provider')
        usercredential = UserCredential.objects.get(id=usercredential_id)

        #_logger.debug("Usercredential. id=[{}] obj:{}".format(usercredential_id, usercredential))

        obj = IaaS.objects.create(
            project = project,
            name = iaas_name,
            inputs = dict( 
                keykind      =  'rsa',
                publickey    =  '',
                privatekey   =  '',
                sshkeyname   =  request.POST.get('f-modal-authentication-key'),
                image        =  f_modal_image,
                stream       =  f_modal_image.get('name', 'unknown'),
                icon         =  f_modal_image.get('iconClass', '/ahome/assets/empty-state.svg'),
                version      =  request.POST.get('f-modal-image-version'),
                plan         =  f_modal_plan,
                storage      =  request.POST.get('f-modal-storage'),
                name         =  request.POST.get('f-modal-name'),
                instance     =  request.POST.get('f-modal-instance'),
                count        =  request.POST.get('f-modal-count'),
                email_secret =  request.POST.get('f-modal-authentication-secret'),
                costs        =  param_value(request, 'f-modal-costs', 0),
                provider     =  request.POST.get('f-modal-provider-kind'),
                options      =  dict(
                    private_networking = request.POST.get('f-modal-option-private-networking'),
                    ipv6               = request.POST.get('f-modal-option-ipv6'),
                    user_data          = request.POST.get('f-modal-option-user-data'),
                    monitoring         = request.POST.get('f-modal-option-monitoring'),
                    backup             = request.POST.get('f-modal-option-backup'),
                    ),
                extrafields = dict(),
                ),
            schema           = dict(),
            applications     = applications,
            kind             = request.POST.get('f-modal-provider-kind'),
            usercredential   = usercredential,
            # tags = request.POST.get('f-modal-tags'),
        )
        obj.save()

# TODO: 'f-modal-authentication-key': [''], 'f-modal-authentication-secret': [''], 'f-modal-project': ['']


# f-modal-instance=ahome-s-2vcpu-96gb-kvm-01&f-modal-count=1&
# f-modal-option-private-networking=false&
# f-modal-option-ipv6=false&
# f-modal-option-user-data=false&
# f-modal-option-monitoring=true&
# f-modal-option-backup=true&f-modal-elk_config_path=https%3A%2F%2Fgitlab.afahounko.com%2Fcommunity%2Felk&f-modal-tags=&f-modal-costs=0.07


# '{'f-modal-image': ["{'image_id': 3, 'name': 'fedora', 'label': 'Fedora', 'iconClass': 'ahome/assets/fedora-icon.svg', 'default': '18 x64', 'version': ['18 x64', '16 x64', '14 x64'], 'group_id': 1}"], 
# 'f-modal-provider': ['2'], 'f-modal-provider-name': [''], 'f-modal-provider-kind': [''], 
# 'f-modal-plan': ["{'plan_id': 1, 'name': '1vcpu_1gb_60gb', 'price': 0.006, 'rate': 'hour', 'vcpu': 1, 'memory': 2, 'disk': 60, 'traffic': 'unlimited traffic', 'device': 'euro'}"], 
# 'f-modal-storage': [''], 'f-modal-authentication-key': [''], 'f-modal-authentication-secret': [''], 'f-modal-project': [''], 
# 'f-modal-name': ['my personal cloud'], 'f-modal-instance': ['freebsd-s-20vcpu-96gb-ams3-01'], 'f-modal-count': ['1'], 
# 'f-modal-tags': ['tags'], 'f-modal-costs': ['4.38']}'


        # f__kind = request.POST.get('ahome_kind')
        # f__form_fields = request.POST.get('ahome_fields')
        # f__form_fields_advanced = request.POST.get('ahome_fields_advanced')
        # f__form_credentials = request.POST.get('ahome_credentials')
        # f__form_credentials_advanced = request.POST.get('ahome_credentials_advanced')

        
        # if f__kind and f__form_fields and f__form_fields_advanced and f__form_credentials and f__form_credentials_advanced:

        #     f__name = request.POST.get('ahome_name', None)
        #     f__id = mk_int(request.POST.get('ahome_instance_id'))
        #     f__credentialsfield = ast.literal_eval(request.POST.get('ahome_credentialsfield'))

        #     f__inputs = dict()
        #     f__schema = dict()
        #     for s in schema_hiddenlist:
        #         hidden_field = ast.literal_eval(request.POST.get( "ahome_{}".format(s) ))
        #         f__schema[s] = hidden_field
        #         for f in hidden_field:

        #             field = "wizardbox-{}".format(f.get('name'))

        #             if request.POST.get(field):
        #                 # save as boolean if key exists
        #                 if f.get('type') == 'checkbox':
        #                     f__inputs[f.get('name')] = bool(request.POST.get(field, None))
        #                 else:
        #                     # save as integer
        #                     if f.get('type') == 'integer':
        #                         f__inputs[f.get('name')] = mk_int( request.POST.get(field) )
        #                     else:
        #                     # finally save as string
        #                         f__inputs[f.get('name')] = request.POST.get(field)
                    
        #             else:
        #                 # save as false if key does not exist or not submitted
        #                 if f.get('type') == 'checkbox':
        #                     f__inputs[f.get('name')] = bool('')
        #             # else:
        #             #     f__inputs[f.get('name')] = None


        #     # f_ahomefile = ast.literal_eval(request.POST.get('ahome_ahomefile'))

        #     if f__id == 0:

        #         usercredential = UserCredential.objects.get( id = f__credentialsfield.get('usercredential') )

        #         obj = IaaS.objects.create(
        #             name = f__name,
        #             inputs = f__inputs,
        #             schema = f__schema,
        #             kind = f__kind,
        #             credentials = f__credentialsfield,
        #             usercredential = usercredential,
        #             )
        #         obj.save()
        #     else:
        #         IaaS.objects.filter( id=f__id ).update(
        #             name = f__name,
        #             inputs = f__inputs,
        #             )


    return JsonResponse(data)


def wizardboxesform_update(request, model, pk, refresh=True):

    instance = dict()
    obj = IaaS.objects.filter(id=pk).values()
    for i in obj:
        instance = i


    defaultform = wizardboxes_json.get("default")

    kind = instance.get("kind")

    ahomefile = generateform(kind)

    schema = instance.get("schema")

    initial = instance.get("inputs")

    if not refresh:
        # pass
        schemafields = schema.get("fields")
        schemafields_advanced = schema.get("fields_advanced")
        schemacredentials = schema.get("credentials")
        schemacredentials_advanced = schema.get("credentials_advanced")

    else:
        # pass
        schemafields = ahomefile.get("fields")
        schemafields_advanced = ahomefile.get("fields_advanced")
        schemacredentials = DICT_CREDENTIALS.get('secret') #ahomefile.get("credentials")
        schemacredentials_advanced = DICT_CREDENTIALS.get('sshkey') #ahomefile.get("credentials_advanced")





    credentialsfield = instance.get("credentials")

    data = render_jsonform(request, kind, schemafields, schemafields_advanced, schemacredentials, schemacredentials_advanced, initial, instance, credentialsfield)


    return JsonResponse(data)




def wizardboxesform_credential(request, kind, pk=0, advanced=0):


    defaultform = wizardboxes_json.get("default")

    # ahomefile = generateform(kind)
    jsonform = DICT_CREDENTIALS.get('secret')

    # credentials = "credentials"
    
    if advanced > 0:
        # credentials = "credentials_advanced"
        jsonform = DICT_CREDENTIALS.get('sshkey')

    # schemacredentials = ahomefile.get(credentials)


    hiddeninputs = dict(
        kind = kind,
        schema = jsonform,
        )

    initial = {}
    if pk > 0:
        dataset = UserSecret.objects.filter(pk=pk).values()

        

        for ds in dataset:    
            if ds:
                initial.update( ds.get('inputs') )

                # _logger.info("Data inputs: '{}' for schema: {}".format(initial, jsonform))

    CONTEXT = { 'credentialform': WizardForm( prefix='wizardbox', jsonform=jsonform, initial=initial ), 'hiddeninputs': hiddeninputs }

    data = dict()
    data['html_form'] = render_to_string('frontend/includes/helpers/wizard-credentialform.html', CONTEXT)

    # _logger.info("Data: '{}'".format(data))

    return JsonResponse(data)




@cache_page(DEFAULT_CACHE_TIME)
def wizardboxesform_retrieve_credential(request, kind, pk, advanced=0):


    defaultform = wizardboxes_json.get("default")


    jsonform = DICT_CREDENTIALS.get('secret')

    # ahomefile = generateform(kind)

    # credentials = "credentials"
    
    if advanced > 0:
        # credentials = "credentials_advanced"
        jsonform = DICT_CREDENTIALS.get('sshkey')

    # schemacredentials = ahomefile.get(credentials)


    hiddeninputs = dict(
        kind = kind,
        schema = jsonform,
        )

    initial = {}

    CONTEXT = { 'credentialform': WizardForm(prefix='wizardbox', jsonform=jsonform, initial=initial), 'hiddeninputs': hiddeninputs }

    data = dict()
    data['html_form'] = render_to_string('frontend/includes/helpers/wizard-credentialform.html', CONTEXT)

    # _logger.info("Data: '{}'".format(data))

    return JsonResponse(data)



def wizardboxes(request):


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)




def wizardboxes_create(request):


    if request.method == 'POST':
        form = ahomeForm(request.POST)
    else:
        form = ahomeForm()

    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


def wizardboxes_update(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)



def wizardboxes_delete(request, pk):


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



@cache_page(DEFAULT_CACHE_TIME)
def wizardboxesform_retrieve_pricing(request, kind, block='plan'):


    wizardboxes_fields = dict()

    
    wizardboxes_fields = get_apidata("wizardboxes", request)


    apidata = get_apidata(API_NAME, request)

    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })

    CONTEXT.update({ 'request': request, })

    CONTEXT.update( dict( api = dict(
        providers = get_apidata('providers', request),
        usercredentials = get_apidata('usercredentials', request),
        usersecrets = get_apidata('usersecrets', request),
        imagegroups     = get_apidata('provisioning/iaac/image_groups/list', request),
        plangroups      = get_apidata('provisioning/iaac/plan_groups/list', request),
        storages        = get_apidata(f'provisioning/iaac/storage/{kind}/list', request),   # hardcoded AWS before setting default storage - TODO
                                ) 
                        )
                    )


    data = dict()
    # data['html_form'] = render_to_string('frontend/includes/helpers/wizard-pricing-plan.html', CONTEXT)

    for item in CONTEXT['api']['plangroups']:
        plan = dict(
            name = item.get('plan_name'),
            desc = item.get('plan_desc'),
            kind = kind,
            )
        CONTEXT.update({ 'plan': plan, })
        data[item.get('plan_name')] = render_to_string('frontend/includes/helpers/wizard-pricing-plan.html', CONTEXT)

    data['storage'] = render_to_string('frontend/includes/helpers/wizard-pricing-storage.html', CONTEXT)

    return JsonResponse(data)



# @cache_page(DEFAULT_CACHE_TIME)
def wizardboxesform_retrieve_additional_fields(request, image):



    ahomefile = generateform(image)

    
    initial = dict()
    
    schemafields = ahomefile.get("fields")
    schemafields_advanced = ahomefile.get("fields_advanced")
    # schemacredentials = DICT_CREDENTIALS.get('secret') #ahomefile.get("credentials")
    # schemacredentials_advanced = DICT_CREDENTIALS.get('sshkey') #ahomefile.get("credentials_advanced")


    f_context = dict(
        wizardboxform = WizardForm(jsonform=schemafields, initial=initial),
        wizardboxform_advanced = WizardForm(prefix='f-form-option', jsonform=schemafields_advanced, initial=initial),
        modalform = WizardForm(prefix='f-modal-option', jsonform=schemafields, initial=initial),
        modalform_advanced = WizardForm(prefix='f-modal-option', jsonform=schemafields_advanced, initial=initial),
        )

    data = dict(
        html_form  = render_to_string('frontend/includes/helpers/wizard-additional-fields.html', f_context),
        modal_form = render_to_string('frontend/includes/helpers/wizard-modal-additional-fields.html', f_context),
        )


    return JsonResponse(data)





