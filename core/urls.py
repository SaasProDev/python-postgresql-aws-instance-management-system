from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from core import views
from account import views as account_views
# from core.views import *  # noqa

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()



# router.register(r'users', UserViewSet)

# router.register(r'organizations', views.OrganizationViewSet, basename="organization")
router.register(r'dashboard', views.DashboardViewSet, basename="dashboard")
#router.register(r'users', views.UserViewSet, basename="user")
#router.register(r'groups', views.GroupViewSet, basename="group")
#router.register(r'permissions', views.PermissionViewSet, basename="permission")
#router.register(r'organizations', views.OrganizationViewSet, basename="organization")
router.register(r'rirs', views.RirViewSet, basename="rir")
router.register(r'vrfs', views.VrfViewSet, basename="vrf")
router.register(r'prefixes', views.PrefixViewSet, basename="prefix")
router.register(r'vlans', views.VlanViewSet, basename="vlan")
router.register(r'aggregates', views.AggregateViewSet, basename="aggregate")
router.register(r'ipaddresses', views.IPAddressViewSet, basename="ipaddress")
router.register(r'devices', views.DeviceViewSet, basename="device")
router.register(r'networkgears', views.NetworkGearViewSet, basename="networkgear")
router.register(r'containers', views.ContainerViewSet, basename="container")
router.register(r'virtualmachines', views.VirtualMachineViewSet, basename="virtualmachine")

router.register(r'providers', views.ProviderViewSet, basename="provider")
router.register(r'iaas', views.IaaSViewSet, basename="iaas")
router.register(r'paas', views.PaaSViewSet, basename="paas")
router.register(r'sdns', views.SdnViewSet, basename="sdn")
router.register(r'storages', views.StorageViewSet, basename="storage")
router.register(r'services', views.ServiceViewSet, basename="service")
router.register(r'monitorings', views.MonitoringViewSet, basename="monitoring")
router.register(r'security', views.SecurityViewSet, basename="security")
router.register(r'pkis', views.PkiViewSet, basename="pki")
router.register(r'backups', views.BackupViewSet, basename="backup")
router.register(r'billings', views.BillingViewSet, basename="billing")
router.register(r'documentations', views.DocumentationViewSet, basename="documentation")
router.register(r'jobs', views.JobViewSet, basename="job")
router.register(r'jobevents', views.JobEventViewSet, basename="jobevent")
router.register(r'wizardboxes', views.WizardBoxesViewSet, basename="wizardbox")

router.register(r'userkeys', views.UserKeyViewSet, basename="userkey")
router.register(r'usersecrets', views.UserSecretViewSet, basename="usersecret")
router.register(r'usercredentials', views.UserCredentialViewSet, basename="usercredential")

# router.register(r'infrastructure', views.InfrastructureViewSet, basename="infrastructure")
router.register(r'projects', views.ProjectViewSet, basename="project")

router.register(r'organizations', account_views.OrganizationViewSet, basename="organization")
router.register(r'users', account_views.UserViewSet, basename="user")
router.register(r'userpermissions', account_views.UserPermisionsInfoViewSet, basename="userpermission")
router.register(r'teams', account_views.TeamViewSet, basename="team")

router.register(r'groups', account_views.GroupViewSet, basename="group")
# router.register(r'permissions', account_views.PermissionViewSet, basename="permission")

router.register(r'runnertasks', views.RunnerTaskViewSet, basename="runnertask")

router.register(r'accessgroups', account_views.AccessGroupViewSet, basename="accessgroup")
router.register(r'accessgrouppermissions', account_views.AccessGroupRulesViewSet, basename="accessgrouppermission")
router.register(r'accessuserpermissions', account_views.AccessUserRulesViewSet, basename="accessuserpermission")

# router.register(r'groups', account_views.GroupViewSet, basename="group")
# router.register(r'permissions', account_views.PermissionViewSet, basename="permission")

# urlpatterns = router.urls


# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', obtain_auth_token),
    url(r'^provisioning/iaac/image_groups/list/', views.ProvisioningIaacImageGroupsViewSet.as_view()),
    # url(r'^provisioning/iaac/distros/', views.ProvisioningIaacImagesViewSet.as_view( {'get': 'list'} )),
    # url(r'^provisioning/iaac/distros/<int:pk>', views.ProvisioningIaacImagesViewSet.as_view( {'get': 'list'} )),
    path('provisioning/iaac/distros/<slug:group>/list/', views.ProvisioningIaacImagesViewSet.as_view( {'get': 'list'} ) , name='provisioning_iaac_distros'),
    url(r'^provisioning/iaac/plan_groups/list/', views.ProvisioningIaacPlanGroupsViewSet.as_view()),
    path('provisioning/iaac/pricing/<slug:provider>/<slug:plan>/list/', views.ProvisioningIaacPlansViewSet.as_view({'get': 'list'}), name='provisioning_iaac_pricing'),
    path('provisioning/iaac/storage/<slug:provider>/list/', views.ProvisioningIaacStoragesViewSet.as_view( {'get': 'list'} ) , name='provisioning_iaac_storage'),
    path('userdashboard/virtualmachines/usage/list/', views.DashboardVirtualMachineStorageUsageViewSet.as_view( {'get': 'list'} ) , name='userdashboard_virtualmachines_usage'),
    # url(r'^provisioning/iaac_pricing/', views.health),
    # url(r'^provisioning/iaac_providers/', views.health),
    # url(r'^provisioning/iaac_storage/', views.health),
    # url(r'^provisioning/image_groups/', views.health),
    url(r'^health$', views.health),
]




# urlpatterns += [
#     url(r'^api-token-auth/', views.obtain_auth_token)
# ]

