import csv
import logging

from datetime import date
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from evaluate_m2.exception_utils import get_evaluate_m2_not_found_exception
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.serializers import EventsViewSerializer

from parse_m2.models import AccountActivity, AccountHolder, Metro2Event
from parse_m2.serializers import AccountActivitySerializer, AccountHolderSerializer

def download_evaluator_metadata(request):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
    filename = f"evaluator-metadata-{date.today()}.csv"
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

    writer = csv.writer(response)

    # Add the header to the CSV response
    writer.writerow(EvaluatorMetadata.csv_header)

    # Add all evaluators to the response
    for eval in EvaluatorMetadata.objects.all():
        writer.writerow(eval.serialize())

    return response

@api_view(('GET',))
def download_evaluator_results_csv(request, event_id, evaluator_id):
    logger = logging.getLogger('views.download_evaluator_results_csv')
    try:
        event = Metro2Event.objects.get(id=event_id)
        eval = EvaluatorMetadata.objects.get(id=evaluator_id)
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=event, evaluator=eval)

        filename = f"{event.name}_{eval.id}_{date.today()}.csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        header_created=False

        writer = csv.writer(response)

        # Add all evaluator results to the response
        for eval_result in eval_result_summary.evaluatorresult_set.all():
            if not header_created:
                # Add the header to the CSV response
                writer.writerow(eval_result.create_csv_header())
                header_created=True
            writer.writerow(eval_result.create_csv_row_data())
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
    try:
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=Metro2Event.objects.get(id=event_id),
            evaluator=EvaluatorMetadata.objects.get(id=evaluator_id))
        results = []
        # Add all evaluator results field_values to the response
        for eval_result in eval_result_summary.evaluatorresult_set.all()[:50]:
            results.append(eval_result.field_values)
        data = {'hits': results}
        return JsonResponse(data)
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
        event_activities=event.get_all_account_activity().filter(
            cons_acct_num=account_number)
        activities_serializer = AccountActivitySerializer(event_activities, many=True)
        eval_results = EvaluatorResult.objects.filter(
            acct_num=account_number,
            result_summary__event=event)
        eval_metadata=[]
        for e in eval_results:
            eval={'id': e.result_summary.evaluator.id,
                'name': e.result_summary.evaluator.name}
            if eval not in eval_metadata:
                eval_metadata.append(eval)
        data = {'cons_acct_num': account_number,
                'inconsistencies': eval_metadata,
                'account_activity': activities_serializer.data}
        return JsonResponse(data)
    except (
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
        result = AccountHolder.objects.filter(
            data_file__event__id=event_id,
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
        eval_result_summary = EvaluatorResultSummary.objects.filter(event=event)
        evaluators = [ers.evaluator for ers in eval_result_summary]
        evaluator_metadata_serializer = EventsViewSerializer(evaluators, many=True)
        result = {
            'id': event.id,
            'name': event.name,
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