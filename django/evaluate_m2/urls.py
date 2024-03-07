from django.urls import path

from evaluate_m2 import views as eval_views


urlpatterns = [
    path('<int:event_id>/evaluator/<str:evaluator_id>/csv',
         eval_views.download_evaluator_results_csv),
    path('<int:event_id>/evaluator/<str:evaluator_id>',
         eval_views.evaluator_results_view),
    path('<int:event_id>/account/<str:account_number>',
         eval_views.account_summary_view),
    path('<int:event_id>/account/<str:account_number>/account_holder',
         eval_views.account_pii_view),
]
