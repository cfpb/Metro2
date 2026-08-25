import csv
import logging
from datetime import date

from django.conf import settings
from django.db import ProgrammingError
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import get_list_or_404
from django.utils.functional import cached_property

import botocore
import django_filters.rest_framework
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_application.s3_utils import s3_session
from evaluate_m2 import upload_utils
from evaluate_m2.exception_utils import (
    format_error,
    get_evaluate_m2_not_found_exception,
)
from evaluate_m2.filters import AccountListFilterSet, EvaluatorResultFilterSet
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)
from evaluate_m2.pagination import EvaluatorResultsPaginator
from evaluate_m2.serializers import (
    AccountListSerializer,
    EvaluatorMetadataSerializer,
    EvaluatorResultSerializer,
    EventsViewSerializer,
)
from evaluate_m2.views_utils import (
    get_object,
    has_permissions_for_request,
)
from parse_m2.models import AccountActivity, Metro2Event
from parse_m2.serializers import AccountActivitySerializer, AccountHolderSerializer


@api_view(("GET",))
def download_evaluator_metadata_csv(request):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
    filename = f"evaluator-metadata-{date.today()}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

    eval_metadata_serializer = EvaluatorMetadataSerializer(
        EvaluatorMetadata.objects.all().order_by('id'),
        many=True,
    )
    header = EvaluatorMetadataSerializer.Meta.fields
    # Add the header to the CSV response
    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()

    # Add all evaluators to the response
    for row in eval_metadata_serializer.data:
        writer.writerow(row)

    return response


@api_view(("GET",))
def download_evaluator_results_csv(request, event_id, evaluator_id):
    logger = logging.getLogger("views.download_evaluator_results_csv")
    try:
        event = Metro2Event.objects.get(id=event_id)
        evaluator = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=evaluator
        )

        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)

        if settings.S3_ENABLED:
            return fetch_csv_results_from_s3(request, event_id, evaluator_id)

        # TODO: fall back on generating the response if the fetch from S3 fails
        else:
            filename = f"{event.name}_{evaluator.id}.csv"
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"},
            )
            return upload_utils.generate_full_csv(eval_result_summary, response)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist,
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)


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


@api_view()
def events_view(request, event_id):
    logger = logging.getLogger("views.evaluator_results_view")
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)

        eval_result_summaries = (
            EvaluatorResultSummary.objects.filter(event=event, hits__gt=0)
            .select_related("evaluator")
            .order_by("evaluator__id")
        )
        evaluator_metadata_serializer = EventsViewSerializer(
            eval_result_summaries, many=True, context={"event": event}
        )
        result = {
            "id": event.id,
            "name": event.name,
            "portfolio": event.portfolio,
            "eid_or_matter_num": event.eid_or_matter_num,
            "other_descriptor": event.other_descriptor,
            "directory": event.directory,
            "date_range_start": event.date_range_start,
            "date_range_end": event.date_range_end,
            "evaluators": evaluator_metadata_serializer.data,
        }
        return Response(result)
    except (Metro2Event.DoesNotExist, EvaluatorResultSummary.DoesNotExist) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)


###########################################
## Helper methods for eval results when S3_ENABLED == True
def fetch_csv_results_from_s3(request, event_id, evaluator_id):
    logger = logging.getLogger("views.fetch_csv_results_from_s3")
    filename = upload_utils.s3_filename(evaluator_id, "csv")
    key = upload_utils.s3_bucket_key(event_id, evaluator_id, "csv")
    try:
        response = StreamingHttpResponse(
            get_object(s3_session(), settings.S3_BUCKET_NAME, key),
            status=200,
            content_type="text/csv",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            error = get_evaluate_m2_not_found_exception(
                e.response["Error"]["Message"],
                event_id,
                evaluator_id,
                request.path,
                None,
            )
            logger.error(error["message"])
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class EvaluatorResultsView(generics.ListAPIView):
    serializer_class = EvaluatorResultSerializer
    pagination_class = EvaluatorResultsPaginator
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    filterset_class = EvaluatorResultFilterSet

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        evaluator_id = self.kwargs["evaluator_id"]
        return EvaluatorResultMaterializedView.objects.filter(
            event_id=event_id,
            evaluator_id=evaluator_id,
        ).order_by("activity_date")

    def get(self, request, *args, **kwargs):
        # Override the default `get()` so we can error appropriately if
        # the event_id or evaluator_id are invalid.
        try:
            return super().get(request, *args, **kwargs)
        except (
            Metro2Event.DoesNotExist,
            EvaluatorMetadata.DoesNotExist,
            EvaluatorResultSummary.DoesNotExist,
        ) as e:
            logger = logging.getLogger("views.download_evaluator_results_csv")
            error = get_evaluate_m2_not_found_exception(
                str(e),
                self.kwargs["event_id"],
                self.kwargs["evaluator_id"],
                request.path,
            )
            logger.error(error["message"])
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        except ProgrammingError as e:
            # Gracefully handle when the materialized view doesn't exist as a 503.
            # It will raise a ProgrammingError, which we introspect to make sure
            # it's caused by an UndefinedTable, otherwise we let it raise.
            import psycopg
            if not isinstance(e.__cause__, psycopg.errors.UndefinedTable):
                raise
            return Response(
                format_error(
                    503,
                    "Not available",
                    "Materialized view for evaluator results is not available",
                    request.path
                ),
                status=503
            )

    def get_sample_queryset(self, queryset):
        event_id = self.kwargs["event_id"]
        evaluator_id = self.kwargs["evaluator_id"]
        # If the Eval Result Summary doesn't exist, this will error,
        # responding with 404 automatically
        EvaluatorResultSummary.objects.get(
            event_id=event_id,
            evaluator__id=evaluator_id
        )

        sample_results = queryset.filter(sample=True)

        if sample_results.exists():
            return sample_results
        else:
            # OR select a random set of sample length from the queryset
            return queryset.order_by("?")[:settings.M2_RESULT_SAMPLE_SIZE]

    def list(self, request, *args, **kwargs):
        # TODO: replace using DRF permissions/check_permissions()
        event_id = self.kwargs["event_id"]
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)

        # Default to sample view
        view_param = self.request.query_params.get("view", "sample")

        if view_param == "sample":
            # Get a sample queryset
            queryset = self.get_sample_queryset(self.get_queryset())
        else:
            # Get the full result set, performing any filtering as needed
            queryset = self.filter_queryset(self.get_queryset())

        # Paginate and serialize results.
        # Pagination size should be the same as the sample size, so the
        # sample view will be exactly one page long.
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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
