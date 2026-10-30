from django.urls import path

from evaluate_m2.views import (
     account_views,
     eval_results_views,
     event_views,
)


# All URLs begin with `/api/events/`
urlpatterns = [
    path('<int:event_id>/evaluator/<str:evaluator_id>/csv/',
         eval_results_views.download_evaluator_results_csv),
    path('<int:event_id>/evaluator/<str:evaluator_id>/',
         eval_results_views.EvaluatorResultsView().as_view()),
    path('<int:event_id>/evaluator/<str:evaluator_id>/facets/',
         eval_results_views.EvaluatorResultsFacetsView().as_view()),
    path('<int:event_id>/account/',
        account_views.AccountsListView().as_view()),
    path('<int:event_id>/account/<str:account_number>/',
        account_views.account_summary_view),
    path('<int:event_id>/account/<str:account_number>/account_holder/',
        account_views.account_pii_view),
     path('<int:event_id>/', event_views.events_view),
]
