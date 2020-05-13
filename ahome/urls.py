"""ahome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from django.urls import path, include
from django.conf import settings


# from admin.site.urls import urls as admin_urls
from frontend import urls as frontend_urls
from core import urls as api_urls
# from socketio_app import urls as socketio_urls


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views as authtoken_views

from django.contrib.auth import views as auth_views

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
    )


# from core.urls import core_router

schema_view = get_schema_view(
   openapi.Info(
      title="Ahome API",
      default_version='v1',
      description="ahome Cloud as a Service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@ahome.africa"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^', include(frontend_urls)),
    # url(r'^socketio/', include(socketio_urls)),
    url(r'^api/v1/', include(api_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authtoken_views.obtain_auth_token),
    
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$',   schema_view.with_ui('redoc', cache_timeout=0),   name='schema-redoc'),
    
    path('admin/', admin.site.urls),
    url( r'^favicon.ico$', RedirectView.as_view( url=staticfiles_storage.url('ahome/assets/favicon.ico'), permanent=False), name="favicon"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('api/<int:version>/', include(core_urls)),
    
]



if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()




# urlpatterns = [
#     url(r'^$', ApiRootView.as_view(), name='api_root_view'),
#     url(r'^(?P<version>(v2))/', include(v2_urls)),
#     url(r'^(?P<version>(v1|v2))/', include(v1_urls)),
#     url(r'^login/$', LoggedLoginView.as_view(
#         template_name='rest_framework/login.html',
#         extra_context={'inside_login_context': True}
#     ), name='login'),
#     url(r'^logout/$', LoggedLogoutView.as_view(
#         next_page='/api/', redirect_field_name='next'
#     ), name='logout'),
#     url(r'^o/', include(oauth2_root_urls)),
# ]
# if settings.SETTINGS_MODULE == 'awx.settings.development':
#     from awx.api.swagger import SwaggerSchemaView
#     urlpatterns += [
#         url(r'^swagger/$', SwaggerSchemaView.as_view(), name='swagger_view'),
#     ]
