import csv
import logging
from datetime import date
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from evaluate_m2.exception_utils import get_eval_results_not_found_exception
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary
from parse_m2.models import Metro2Event

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

@api_view()
def download_evaluator_results_csv(request, event_id, evaluator_name):
    logger = logging.getLogger('views.download_evaluator_results_csv')
    try:
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=Metro2Event.objects.get(id=event_id),
            evaluator=EvaluatorMetadata.objects.get(name=evaluator_name))
        filename = f"{eval_result_summary.event.name}_{evaluator_name}_{date.today()}.csv"
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
            else:
                writer.writerow(eval_result.create_csv_row_data())
        return response
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_eval_results_not_found_exception(str(e), event_id, evaluator_name, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)

@api_view()
def download_evaluator_results(request, event_id, evaluator_name):
    logger = logging.getLogger('views.download_evaluator_results')
    try:
        eval_result_summary = EvaluatorResultSummary.objects.get(
            event=Metro2Event.objects.get(id=event_id),
            evaluator=EvaluatorMetadata.objects.get(name=evaluator_name))
        results = []
        # Add all evaluator results field_values to the response
        for eval_result in eval_result_summary.evaluatorresult_set.all():
            results.append(eval_result.field_values)
        data = {'hits': results}
        return JsonResponse(data)
    except (
        Metro2Event.DoesNotExist,
        EvaluatorMetadata.DoesNotExist,
        EvaluatorResultSummary.DoesNotExist
    ) as e:
        error = get_eval_results_not_found_exception(str(e), event_id, evaluator_name, request.path)
        logger.error(error['message'])
        return Response(error, status=status.HTTP_404_NOT_FOUND)
