import csv
from django.http import HttpResponse
from datetime import date
from django.shortcuts import render
from evaluate_m2.models import EvaluatorMetadata


def download_evaluator_metadata(request):
    # Documentation on returning CSV: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
    filename = f"evaluator-metadata-{date.today()}.csv"
    response = HttpResponse(
        content_type="test/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

    writer = csv.writer(response)

    # Add the header to the CSV response
    writer.writerow(EvaluatorMetadata.csv_header)

    # Add all evaluators to the response
    for eval in EvaluatorMetadata.objects.all():
        writer.writerow(eval.serialize())

    return response
