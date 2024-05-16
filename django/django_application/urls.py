"""
URL configuration for m2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from users import views
from evaluate_m2 import views as eval_views
from evaluate_m2 import urls as evaluate_m2_urls
from django_application import views as error_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/all-evaluator-metadata/', eval_views.download_evaluator_metadata_csv),
    path('api/events/', include(evaluate_m2_urls)),
    path('api/users/', views.users_view),
    path('api/users/<int:user_id>/', views.users_view)
]

try:
    # If the SSO library is installed, include auth-related URLs
    urlpatterns += [
        path('oauth2/', include('django_auth_adfs.urls')),
    ]
except ImproperlyConfigured:
    pass
# Handles fall through route for all erroneous api calls to return bad request
urlpatterns.append(re_path(r'api(?:.*)?', error_view.bad_request_view ))

# Fall through route to handle all other urls through front end
urlpatterns.append(re_path(r'^(?:.*)?', TemplateView.as_view(template_name='m2/index.html')))
