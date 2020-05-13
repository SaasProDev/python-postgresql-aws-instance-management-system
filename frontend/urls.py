from django.urls import path, include
from django.views.generic.base import TemplateView

from django.contrib.auth import views as auth_views

# import .views
# from . import views
# from frontend.views import *
from .views.index import *
from .views.dashboard import *
from .views.organizations import *
from .views.projects import *
from .views.rirs import *
from .views.vrfs import *
from .views.aggregates import *
from .views.backups import *
from .views.billings import *
from .views.containers import *
from .views.devices import *
from .views.documentations import *
from .views.ipaddresses import *
from .views.monitorings import *
from .views.pkis import *
from .views.prefixes import *
from .views.providers import *
from .views.iaas import *
from .views.paas import *
from .views.sdns import *
from .views.security import *
from .views.services import *
from .views.settings import *
from .views.storages import *
from .views.virtualmachines import *
from .views.vlans import *
from .views.networkgears import *
from .views.console import *
from .views.credentials import *
from .views.wizardboxes import *
from .views.tokens import *
from .views.users import *
from .views.userkeys import *
from .views.usercredentials import *
from .views.usersecrets import *
from .views.userpreferences import *

#from .views.singlevm import *


jsonform = """
{
  "schema": {
  "message": {
    "type": "string",
    "title": "Message"
  },
  "author": {
    "type": "object",
    "title": "Author",
    "properties": {
      "name": {
        "type": "string",
        "title": "Name"
      },
      "gender": {
        "type": "string",
        "title": "Gender",
        "enum": [ "male", "female", "alien" ]
      },
      "magic": {
        "type": "integer",
        "title": "Magic number",
        "default": 42
      }
    }
  }
},
  "form": [
    "*",
  ],
  "value": { "name": "AFAHOUNKO Danny", "gender": "alien", "age": 34
  }
}
"""



"""
{
  "message": {
    "type": "string",
    "title": "Message"
  },
  "author": {
    "type": "object",
    "title": "Author",
    "properties": {
      "name": {
        "type": "string",
        "title": "Name"
      },
      "gender": {
        "type": "string",
        "title": "Gender",
        "enum": [ "male", "female", "alien" ]
      },
      "magic": {
        "type": "integer",
        "title": "Magic number",
        "default": 42
      }
    }
  }
}
"""


urlpatterns = [

    # path('', views.organizations.index, name='index'),
    path('', index, name='index'),
    # path('frontend/', TemplateView.as_view(template_name="frontend/main.html"), name='frontend_main'),

    path('frontend/dashboard/', dashboard, name='dashboard'),
    path('frontend/dashboard/user/', dashboard_user, name='dashboard_user'),

    path('frontend/accounts/', include('django.contrib.auth.urls')),
    
    path('frontend/tokens/login/', token_login, name='login'),
    path('frontend/tokens/logout/', token_logout, name='logout'),
    path('frontend/tokens/logout/', token_logout, name='password_reset'),
    # path('frontend/users/logout/', auth_views.LoginView.as_view(template_name='frontend/includes/login/index.html'), name='password_reset'),

    path('frontend/users/', users, name='user'),
    path('frontend/users/list/', users_list, name='user_list'),
    path('frontend/users/create/', users_create, name='user_create'),
    path('frontend/users/<int:pk>/update/', users_update, name='user_update'),
    path('frontend/users/<int:pk>/delete/', users_delete, name='user_delete'),


    
    path('frontend/organizations/', organizations, name='organization'),
    path('frontend/organizations/list/', organizations_list, name='organization_list'),
    path('frontend/organizations/create/', organizations_create, name='organization_create'),
    path('frontend/organizations/<int:pk>/update/', organizations_update, name='organization_update'),
    path('frontend/organizations/<int:pk>/delete/', organizations_delete, name='organization_delete'),

    path('frontend/projects/', projects, name='project'),
    path('frontend/projects/list/', project_list, name='project_list'),
    path('frontend/projects/create/', project_create, name='project_create'),
    path('frontend/projects/<int:pk>/update/', project_update, name='project_update'),
    path('frontend/projects/<int:pk>/delete/', project_delete, name='project_delete'),

    path('frontend/rirs/', rirs, name='rir'),
    path('frontend/rirs/list/', rirs_list, name='rir_list'),
    path('frontend/rirs/create/', rirs_create, name='rir_create'),
    path('frontend/rirs/<int:pk>/update/', rirs_update, name='rir_update'),
    path('frontend/rirs/<int:pk>/delete/', rirs_delete, name='rir_delete'),


    path('frontend/vrfs/', vrfs, name='vrf'),
    path('frontend/vrfs/list/', vrfs_list, name='vrf_list'),
    path('frontend/vrfs/create/', vrfs_create, name='vrf_create'),
    path('frontend/vrfs/<int:pk>/update/', vrfs_update, name='vrf_update'),
    path('frontend/vrfs/<int:pk>/delete/', vrfs_delete, name='vrf_delete'),


    path('frontend/prefixes/', prefixes, name='prefix'),
    path('frontend/prefixes/list/', prefixes_list, name='prefix_list'),
    path('frontend/prefixes/create/', prefixes_create, name='prefix_create'),
    path('frontend/prefixes/<int:pk>/update/', prefixes_update, name='prefix_update'),
    path('frontend/prefixes/<int:pk>/delete/', prefixes_delete, name='prefix_delete'),


    path('frontend/aggregates/', aggregates, name='aggregate'),
    path('frontend/aggregates/list/', aggregates_list, name='aggregate_list'),
    path('frontend/aggregates/create/', aggregates_create, name='aggregate_create'),
    path('frontend/aggregates/<int:pk>/update/', aggregates_update, name='aggregate_update'),
    path('frontend/aggregates/<int:pk>/delete/', aggregates_delete, name='aggregate_delete'),


    path('frontend/vlans/', vlans, name='vlan'),
    path('frontend/vlans/list/', vlans_list, name='vlan_list'),
    path('frontend/vlans/create/', vlans_create, name='vlan_create'),
    path('frontend/vlans/<int:pk>/update/', vlans_update, name='vlan_update'),
    path('frontend/vlans/<int:pk>/delete/', vlans_delete, name='vlan_delete'),


    path('frontend/ipaddresses/', ipaddresses, name='ipaddress'),
    path('frontend/ipaddresses/list/', ipaddresses_list, name='ipaddress_list'),
    path('frontend/ipaddresses/create/', ipaddresses_create, name='ipaddress_create'),
    path('frontend/ipaddresses/<int:pk>/update/', ipaddresses_update, name='ipaddress_update'),
    path('frontend/ipaddresses/<int:pk>/delete/', ipaddresses_delete, name='ipaddress_delete'),




    path('frontend/devices/', devices, name='device'),
    path('frontend/devices/list/', devices_list, name='device_list'),
    path('frontend/devices/create/', devices_create, name='device_create'),
    path('frontend/devices/<int:pk>/update/', devices_update, name='device_update'),
    path('frontend/devices/<int:pk>/credential/', devices_credential, name='device_credential'),
    path('frontend/devices/<int:pk>/delete/', devices_delete, name='device_delete'),



    path('frontend/virtualmachines/', virtualmachines, name='virtualmachine'),
    path('frontend/virtualmachines/list/', virtualmachines_list, name='virtualmachine_list'),
    path('frontend/virtualmachines/create/', virtualmachines_create, name='virtualmachine_create'),
    path('frontend/virtualmachines/<int:pk>/update/', virtualmachines_update, name='virtualmachine_update'),
    path('frontend/virtualmachines/<int:pk>/credential/', virtualmachines_credential, name='virtualmachine_credential'),
    path('frontend/virtualmachines/<int:pk>/delete/', virtualmachines_delete, name='virtualmachine_delete'),
    path('frontend/virtualmachines/<int:pk>/detail/', virtualmachines_detail, name='virtualmachine_detail'),

    path('frontend/containers/', containers, name='container'),
    path('frontend/containers/list/', containers_list, name='container_list'),
    path('frontend/containers/create/', containers_create, name='container_create'),
    path('frontend/containers/<int:pk>/update/', containers_update, name='container_update'),
    path('frontend/containers/<int:pk>/delete/', containers_delete, name='container_delete'),


    path('frontend/networkgears/', networkgears, name='networkgear'),
    path('frontend/networkgears/list/', networkgears_list, name='networkgear_list'),
    path('frontend/networkgears/create/', networkgears_create, name='networkgear_create'),
    path('frontend/networkgears/<int:pk>/update/', networkgears_update, name='networkgear_update'),
    path('frontend/networkgears/<int:pk>/delete/', networkgears_delete, name='networkgear_delete'),


    path('frontend/providers/', providers, name='provider'),
    path('frontend/providers/list/', providers_list, name='provider_list'),
    path('frontend/providers/create/', providers_create, name='provider_create'),
    path('frontend/providers/<int:pk>/update/', providers_update, name='provider_update'),
    path('frontend/providers/<int:pk>/credential/', providers_credential, name='provider_credential'),
    path('frontend/providers/<int:pk>/delete/', providers_delete, name='provider_delete'),


    path('frontend/vm/connect/', iaas_vmconnect, name='vmconnect'),

    path('frontend/iaas/', iaas, name='iaas'),
    path('frontend/iaas/list/', iaas_list, name='iaas_list'),
    #path('frontend/iaas/list_pagination/<int:pk>', iaas_list_with_pagination, name='iaas_list_with_pagination'),
    path('frontend/iaas/create/', iaas_create, name='iaas_create'),
    path('frontend/iaas/wizardbox/create/', iaas_wizardbox_create, name='iaas_wizardbox_create'),
    path('frontend/iaas/<int:pk>/update/', iaas_update, name='iaas_update'),
    path('frontend/iaas/<int:pk>/delete/', iaas_delete, name='iaas_delete'),


    path('frontend/paas/', paas, name='paas'),
    path('frontend/paas/list/', paas_list, name='paas_list'),
    path('frontend/paas/create/', paas_create, name='paas_create'),
    path('frontend/paas/wizardbox/create/', paas_wizardbox_create, name='paas_wizardbox_create'),
    path('frontend/paas/<int:pk>/update/', paas_update, name='paas_update'),
    path('frontend/paas/<int:pk>/delete/', paas_delete, name='paas_delete'),
    path('frontend/paas/detail/', paas_detail, name='paas_detail'),
    path('frontend/paas/platforms/', paas_platforms, name='paas_platforms'),


    path('frontend/sdns/', sdns, name='sdn'),
    path('frontend/sdns/list/', sdns_list, name='sdn_list'),
    path('frontend/sdns/create/', sdns_create, name='sdn_create'),
    path('frontend/sdns/<int:pk>/update/', sdns_update, name='sdn_update'),
    path('frontend/sdns/<int:pk>/delete/', sdns_delete, name='sdn_delete'),

    path('frontend/storages/', storages, name='storage'),
    path('frontend/storages/list/', storages_list, name='storage_list'),
    path('frontend/storages/create/', storages_create, name='storage_create'),
    path('frontend/storages/<int:pk>/update/', storages_update, name='storage_update'),
    path('frontend/storages/<int:pk>/delete/', storages_delete, name='storage_delete'),


    path('frontend/services/', services, name='service'),
    path('frontend/services/list/', services_list, name='service_list'),
    path('frontend/services/create/', services_create, name='service_create'),
    path('frontend/services/<int:pk>/update/', services_update, name='service_update'),
    path('frontend/services/<int:pk>/delete/', services_delete, name='service_delete'),


    path('frontend/monitorings/', monitorings, name='monitoring'),
    path('frontend/monitorings/list/', monitorings_list, name='monitoring_list'),
    path('frontend/monitorings/create/', monitorings_create, name='monitoring_create'),
    path('frontend/monitorings/wizardbox/create/', monitorings_wizardbox_create, name='monitorings_wizardbox_create'),
    path('frontend/monitorings/<int:pk>/update/', monitorings_update, name='monitoring_update'),
    path('frontend/monitorings/<int:pk>/delete/', monitorings_delete, name='monitoring_delete'),


    path('frontend/pkis/', pkis, name='pki'),
    path('frontend/pkis/list/', pkis_list, name='pki_list'),
    path('frontend/pkis/create/', pkis_create, name='pki_create'),
    path('frontend/pkis/<int:pk>/update/', pkis_update, name='pki_update'),
    path('frontend/pkis/<int:pk>/delete/', pkis_delete, name='pki_delete'),


    path('frontend/security/', security, name='security'),
    path('frontend/security/list/', security_list, name='security_list'),
    path('frontend/security/create/', security_create, name='security_create'),
    path('frontend/security/<int:pk>/update/', security_update, name='security_update'),
    path('frontend/security/<int:pk>/delete/', security_delete, name='security_delete'),


    path('frontend/backups/', backups, name='backup'),
    path('frontend/backups/list/', backups_list, name='backup_list'),
    path('frontend/backups/create/', backups_create, name='backup_create'),
    path('frontend/backups/<int:pk>/update/', backups_update, name='backup_update'),
    path('frontend/backups/<int:pk>/delete/', backups_delete, name='backup_delete'),


    path('frontend/billings/', billings, name='billing'),
    path('frontend/billings/list/', billings_list, name='billing_list'),
    path('frontend/billings/create/', billings_create, name='billing_create'),
    path('frontend/billings/<int:pk>/update/', billings_update, name='billing_update'),
    path('frontend/billings/<int:pk>/delete/', billings_delete, name='billing_delete'),


    path('frontend/documentations/', documentations, name='documentation'),
    path('frontend/documentations/list/', documentations_list, name='documentation_list'),
    path('frontend/documentations/create/', documentations_create, name='documentation_create'),
    path('frontend/documentations/<int:pk>/update/', documentations_update, name='documentation_update'),
    path('frontend/documentations/<int:pk>/delete/', documentations_delete, name='documentation_delete'),


    path('frontend/credentials/', credentials, name='credential'),
    path('frontend/credentials/create/', credentials_create, name='credential_create'),
    path('frontend/credentials/forms/<slug:kind>/', credentials_form, name='credential_form'),
    path('frontend/credentials/<int:pk>/update/', credentials_update, name='credential_update'),
    path('frontend/credentials/<int:pk>/delete/', credentials_delete, name='credential_delete'),


    path('frontend/wizardboxes/forms/<slug:kind>/<slug:model>/generate/', wizardboxesform_provider, name='wizardboxesform_provider'),
    path('frontend/wizardboxes/forms/<slug:kind>/<slug:model>/<int:pk>/generate/', wizardboxesform_generate, name='wizardboxesform_generate'),
    path('frontend/wizardboxes/forms/<slug:model>/<slug:kind>/save/', wizardboxesform_save, name='wizardboxesform_save'),
    path('frontend/wizardboxes/formsgeneric/save/', wizardGenericform_save, name='wizardGenericform_save'),
    path('frontend/wizardboxes/forms/<slug:model>/<int:pk>/update/', wizardboxesform_update, name='wizardboxesform_update'),
    path('frontend/wizardboxes/credentials/<slug:kind>/pk/<int:pk>/advanced/<int:advanced>/', wizardboxesform_credential, name='wizardboxesform_credential'),

    path('frontend/wizardboxes/pricing/<slug:kind>/<slug:block>/generate/', wizardboxesform_retrieve_pricing, name='wizardboxesform_retrieve_pricing'),

    path('frontend/wizardboxes/fields/<slug:image>/generate/', wizardboxesform_retrieve_additional_fields, name='wizardboxesform_retrieve_additional_fields'),




    
    



    path('frontend/settings/', settings, name='settings'),
    # path('frontend/settings-user-credentials/', settings_user_credentials, name='settings_user_credentials'),
    

    path('frontend/userkeys/', userkeys, name='userkey'),
    path('frontend/userkeys/list/', userkeys_list, name='userkey_list'),
    path('frontend/userkeys/create/', userkeys_create, name='userkey_create'),
    path('frontend/userkeys/<int:pk>/update/', userkeys_update, name='userkey_update'),
    path('frontend/userkeys/<int:pk>/delete/', userkeys_delete, name='userkey_delete'),


    path('frontend/usercredentials/', usercredentials, name='usercredential'),
    path('frontend/usercredentials/list/', usercredentials_list, name='usercredential_list'),
    path('frontend/usercredentials/create/', usercredentials_create, name='usercredential_create'),
    path('frontend/usercredentials/<int:pk>/update/', usercredentials_update, name='usercredential_update'),
    path('frontend/usercredentials/<int:pk>/credential/', usercredentials_credential, name='usercredential_credential'),
    path('frontend/usercredentials/<int:pk>/delete/', usercredentials_delete, name='usercredential_delete'),



    path('frontend/usersecrets/', usersecrets, name='usersecret'),
    path('frontend/usersecrets/list/', usersecrets_list, name='usersecret_list'),
    path('frontend/usersecrets/forms/<slug:kind>/', usersecrets_form, name='usersecret_form'),
    path('frontend/usersecrets/create/', usersecrets_create, name='usersecret_create'),
    path('frontend/usersecrets/<int:pk>/update/', usersecrets_update, name='usersecret_update'),
    path('frontend/usersecrets/<int:pk>/credential/', usersecrets_credential, name='usersecret_credential'),
    path('frontend/usersecrets/<int:pk>/delete/', usersecrets_delete, name='usersecret_delete'),


    path('frontend/console/', console, name='console'),

    path('frontend/userpreferences/', userpreferences, name='userpreference'),

    # path('tasks', GenerateRandomVirtualMachinesView, name='demo_tasks'),
    # path('tasks', GenerateRandomVirtualMachinesView.as_view(), name='demo-tasks'),

    path('demo', TemplateView.as_view(template_name="frontend/trash/demo.html", extra_context={'pagename': 'about', 'jsonform': jsonform}), name='frontend_demo'),


    # path('frontend/demo', views.demo, name='demo'),


    # path('frontend/organizations', TemplateView.as_view(template_name="frontend/organizations.html"), name='frontend_organizations'),
    
    # Simple Virtual machine path
    #path('frontend/dashboard/', singlevm, name='singlevm'),


]


