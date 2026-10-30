import csv
import logging
from datetime import date

from django.conf import settings
from django.db import ProgrammingError
from django.db.models import Count
from django.http import Http404, HttpResponse, StreamingHttpResponse

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
from evaluate_m2.filters import (
    AnyCharFilter,
    EvaluatorResultFilterSet,
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResultMaterializedView,
    EvaluatorResultSummary,
)
from evaluate_m2.pagination import EvaluatorResultsPaginator
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EvaluatorResultSerializer,
)
from evaluate_m2.views.views_utils import (
    get_object,
    has_permissions_for_request,
)
from parse_m2.models import  Metro2Event


@api_view(("GET",))
def download_evaluator_results_csv(request, event_id, evaluator_id):
    logger = logging.getLogger("views.download_evaluator_results_csv")
    try:
        event = Metro2Event.objects.get(id=event_id)
        evaluator = EvaluatorMetadata.objects.get(id=evaluator_id)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path
        )
        logger.error(error["message"])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

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
        qs =  EvaluatorResultMaterializedView.objects.filter(
            event_id=event_id,
            evaluator_id=evaluator_id,
        ).order_by("activity_date")

        return upload_utils.generate_eval_results_csv(qs, response)



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


class EvaluatorResultsFacetsView(generics.GenericAPIView):
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
        )

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs["event_id"]
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse("Unauthorized", status=401)

        # Filter the queryset, this way we compute facets to just what is
        # available in the filtered results
        queryset = self.filter_queryset(self.get_queryset())

        # Get a list of facet-able fields from the filterset.
        # Right now this just facets AnyCharFilter fields, so the JSON field
        # cons_info_ind_assoc isn't supported for facets yet.
        facet_fields = {
            param: declared.field_name
            for param, declared in self.filterset_class.base_filters.items()
            if isinstance(declared, AnyCharFilter)
        }

        # Evaluate the queryset for facets
        # TODO: right now this performs a new query for every facet field, so
        # if there's 10 in FACET_FIELDS, you'll get 10 queries.
        facets = {}
        for param, field_name in facet_fields.items():
            # Have the database calculate a count for each facet field's value
            counts = queryset.values(
                field_name
            ).annotate(
                count=Count('id')
            ).order_by(
                field_name
            )
            # Build a dictionary for this field that is {value: count} for
            # each of its possible values. Set that as the value for the field
            # in the facets dictionary.
            facets[param] = {
                (row[field_name] if row[field_name] not in (None, "") else "blank"):
                    row["count"]
                for row in counts
            }

        # Return a total count and the facet counts
        return Response(
            {
                "count": queryset.count(),
                "facets": facets,
            }
        )