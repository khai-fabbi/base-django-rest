"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

import os

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{settings.API_ENTRY_POINT}', include('apps.authen.urls')),
    path(f'{settings.API_ENTRY_POINT}', include('apps.api.urls')),
]

if settings.DEBUG:
    def log(request):
        log_file_path = os.path.join(settings.LOG_DIRECTORY_PATH, settings.LOG_LEVEL.lower() + '.log')
        response = HttpResponse()

        with open(log_file_path, 'rb') as f:
            lines = f.readlines()[-100:]
            response.write('<pre style="font-family: sans-serif;">' + '\n'.join([line.decode("utf-8") for line in lines]) + '</pre>')

        return response

    schema_view = get_schema_view(
        info=openapi.Info(
            title="API",
            default_version='v1',
            description="This is API description for server. Only use this in development.",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = urlpatterns + [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('log/', log, name='log'),
    ]
