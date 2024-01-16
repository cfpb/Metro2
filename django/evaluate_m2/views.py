import csv
from django.http import HttpResponse
from datetime import date

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

def download_evaluator_results(request, event_id, evaluator_name):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/ noutputting-csv/
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
