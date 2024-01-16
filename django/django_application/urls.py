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
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from users import views
from evaluate_m2 import views as eval_views


urlpatterns = [
    path("", TemplateView.as_view(template_name="m2/index.html")),
    path('admin/', admin.site.urls),
    path('unsecured/', views.unsecured_view),
    path('secured/', views.secured_view),
    path('datasets/', views.datasets),
    path('datasets/<int:dataset_id>/', views.dataset),
    path('all-evaluator-metadata/', eval_views.download_evaluator_metadata),
    path('oauth2/', include('django_auth_adfs.urls')),
]
