import csv
from datetime import date

from django.http import HttpResponse

from rest_framework.decorators import api_view

from evaluate_m2.models import (
    EvaluatorMetadata,
)
from evaluate_m2.serializers import (
    EvaluatorMetadataSerializer,
)


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