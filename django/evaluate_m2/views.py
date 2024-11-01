import csv
import logging

from datetime import date
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from django.core.exceptions import FieldError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from evaluate_m2.views_utils import (
    has_permissions_for_request,
    random_sample_id_list
)
from evaluate_m2.exception_utils import get_evaluate_m2_not_found_exception
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
    EventsViewSerializer)
from parse_m2.models import AccountActivity, AccountHolder, Metro2Event
from parse_m2.serializers import AccountActivitySerializer, AccountHolderSerializer

@api_view(('GET',))
def download_evaluator_metadata_csv(request):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
    filename = f"evaluator-metadata-{date.today()}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

    eval_metadata_serializer = EvaluatorMetadataSerializer(
        EvaluatorMetadata.objects.all(), many=True
    )
    header = EvaluatorMetadataSerializer.Meta.fields
    # Add the header to the CSV response
    writer = csv.DictWriter(response, fieldnames=header)
    writer.writeheader()

    # Add all evaluators to the response
    for row in eval_metadata_serializer.data:
        writer.writerow(row)

    return response

@api_view(('GET',))
def download_evaluator_results_csv(request, event_id, evaluator_id):
    logger = logging.getLogger('views.download_evaluator_results_csv')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        eval = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=eval)

        filename = f"{event.name}_{eval.id}.csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        header_created=False

        writer = csv.writer(response)
        fields_list = eval.result_summary_fields()
        # Add all evaluator results to the response
        for eval_result in eval_result_summary.evaluatorresult_set.all():
            if not header_created:
                # Add the header to the CSV response
                writer.writerow(eval_result.create_csv_header())
                header_created=True
            writer.writerow(eval_result.create_csv_row_data(fields_list))
        return response
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view()
def evaluator_results_view(request, event_id, evaluator_id):
    logger = logging.getLogger('views.evaluator_results_view')
    RESULTS_PAGE_SIZE = 20
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)

        evaluator = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=evaluator)

        id_list = random_sample_id_list(eval_result_summary, RESULTS_PAGE_SIZE)

        try:
            # TODO: update the metadata importer to ensure that
            # result_summary_fields are always valid AccountActivity field names
            result = AccountActivity.objects.filter(id__in=id_list) \
                .values(*evaluator.result_summary_fields())
        except FieldError as e:
            err = f"Metadata for {evaluator.id} has incorrect field name: {e}"
            return Response(err, status=status.HTTP_404_NOT_FOUND)

        response = {'hits': [obj for obj in result]}
        return JsonResponse(response)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, evaluator_id, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(('GET',))
def account_summary_view(request, event_id, account_number):
    logger = logging.getLogger('views.account_summary_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        event_activities=get_list_or_404(event.get_all_account_activity().filter(
            cons_acct_num=account_number).order_by('activity_date'))
        if not event_activities:
            raise Http404()
        activities_serializer = AccountActivitySerializer(event_activities, many=True)
        eval_results = EvaluatorResult.objects.filter(
            acct_num=account_number,
            result_summary__event=event)
        eval_metadata=[]
        for e in eval_results:
            eval=e.result_summary.evaluator.id
            if eval not in eval_metadata:
                eval_metadata.append(eval)
        data = {'cons_acct_num': account_number,
                'inconsistencies': eval_metadata,
                'account_activity': activities_serializer.data}
        return JsonResponse(data)
    except (
        Http404,
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResult.DoesNotExist,
        AccountActivity.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view(('GET',))
def account_pii_view(request, event_id, account_number):
    logger = logging.getLogger('views.account_pii_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        result = AccountHolder.objects.filter(
            data_file__event=event,
            cons_acct_num=account_number).latest('activity_date')
        acct_holder_serializer = AccountHolderSerializer(result)
        return JsonResponse(acct_holder_serializer.data)
    except (
        Metro2Event.DoesNotExist,
        AccountHolder.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path, account_number)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view()
def events_view(request, event_id):
    logger = logging.getLogger('views.evaluator_results_view')
    try:
        event = Metro2Event.objects.get(id=event_id)
        if not has_permissions_for_request(request, event):
            return HttpResponse('Unauthorized', status=401)
        eval_result_summary = EvaluatorResultSummary.objects \
            .filter(event=event, hits__gt=0).order_by('evaluator__id')
        evaluators = [ers.evaluator for ers in eval_result_summary]
        evaluator_metadata_serializer = EventsViewSerializer(
            evaluators, many=True, context={'event': event})
        result = {
            'id': event.id,
            'name': event.name,
            'portfolio': event.portfolio,
            'eid_or_matter_num': event.eid_or_matter_num,
            'other_descriptor': event.other_descriptor,
            'directory': event.directory,
            'date_range_start': event.date_range_start,
            'date_range_end': event.date_range_end,
            'evaluators': evaluator_metadata_serializer.data
        }
        return JsonResponse(result)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_evaluate_m2_not_found_exception(
            str(e), event_id, None, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
