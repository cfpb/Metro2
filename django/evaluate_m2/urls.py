from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from users import views
from evaluate_m2 import views as eval_views


urlpatterns = [
    path('<int:event_id>/evaluator/<str:evaluator_name>/csv', eval_views.download_evaluator_results_csv),
    path('<int:event_id>/evaluator/<str:evaluator_name>', eval_views.download_evaluator_results),
]
