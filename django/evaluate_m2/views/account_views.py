import logging

from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404
from django.utils.functional import cached_property

import django_filters.rest_framework
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from evaluate_m2.exception_utils import (
    get_evaluate_m2_not_found_exception,
)
from evaluate_m2.filters import (
    AccountListFilterSet,
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
)
from evaluate_m2.serializers import (
    AccountListSerializer,
)
from evaluate_m2.views.views_utils import (
    has_permissions_for_request,
)
from parse_m2.models import AccountActivity, Metro2Event
from parse_m2.serializers import AccountActivitySerializer, AccountHolderSerializer


@api_view(("GET",))
def account_summary_view(request, event_id, account_number):
    logger = logging.getLogger("views.account_summary_view")
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)
        event_activities = get_list_or_404(
            event.get_all_account_activity()
            .filter(cons_acct_num=account_number)
            .order_by("activity_date")
            .select_related("k2", "k4", "l1")
        )
        if not event_activities:
            raise Http404()
        activities_serializer = AccountActivitySerializer(event_activities, many=True)

        eval_results = EvaluatorResult.objects.filter(
            acct_num=account_number, result_summary__event=event
        ).select_related("result_summary")
        evals_hit = [e.result_summary.evaluator_id for e in eval_results]
        evals_hit_uniq = sorted(list(set(evals_hit)))

        data = {
            "cons_acct_num": account_number,
            "inconsistencies": evals_hit_uniq,
            "account_activity": activities_serializer.data,
        }
        return Response(data)
    except (
        Http404,
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResult.DoesNotExist,
        AccountActivity.DoesNotExist,
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)


@api_view(("GET",))
def account_pii_view(request, event_id, account_number):
    logger = logging.getLogger("views.account_pii_view")
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)
        latest_acct_activity = AccountActivity.objects.filter(
            data_file__event=event, cons_acct_num=account_number
        ).latest("activity_date")
        acct_holder_serializer = AccountHolderSerializer(latest_acct_activity)
        return Response(acct_holder_serializer.data)
    except (Metro2Event.DoesNotExist, AccountActivity.DoesNotExist) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)


class AccountsListView(generics.ListAPIView):
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    filterset_class = AccountListFilterSet

    @cached_property
    def event(self):
        event_id = self.kwargs["event_id"]
        return Metro2Event.objects.get(id=event_id)

    def get_queryset(self):
        return (
            self.event.get_all_account_activity()
            .only('cons_acct_num', 'port_type', 'acct_type')
            .with_hit_count(self.event)
            .with_record_count(self.event)
        )

    def list(self, request, *args, **kwargs):
        # TODO: replace using DRF permissions/check_permissions()
        if not has_permissions_for_request(request, self.event):
            return HttpResponse("Unauthorized", status=401)

        queryset = self.filter_queryset(self.get_queryset()).distinct_accounts()

        serializer = AccountListSerializer(queryset, many=True)
        return Response(serializer.data)