import csv
import logging

from django.conf import settings
from django.db.models.query import QuerySet

from smart_open import open

from django_application.s3_utils import s3_session
from evaluate_m2.field_names import M2_FIELD_NAMES
from evaluate_m2.models import EvaluatorResultSummary
from evaluate_m2.models import EvaluatorResultMaterializedView


def stream_results_files_to_s3(result_summary: EvaluatorResultSummary):
    stream_full_results_csv_to_s3(result_summary)

##############
# Methods for generating and uploading full CSV
def stream_full_results_csv_to_s3(
    result_summary: EvaluatorResultSummary, url: str = None
):
    """
    Save the results for this evaluator to an S3 bucket.
    """
    event_id = result_summary.event_id
    eval_id = result_summary.evaluator_id

    logger = logging.getLogger('evaluate.stream_full_results_csv_to_s3')
    if not url:
        url = full_s3_url(event_id, eval_id, 'csv')

    logger.info(
        f"Saving results CSV for event {event_id}, evaluator {eval_id}"
    )

    results_set = EvaluatorResultMaterializedView.objects.filter(
        event_id = event_id, evaluator_id=eval_id,
    )
    with open(url, 'w', transport_params={'client': s3_session()}) as fout:
        generate_eval_results_csv(results_set, fout)
    logger.debug("Completed saving CSV file")

def csv_header_row(columns: list[str]) -> str:
    """
    Translate the list of fields to their human-friendly names.
    """
    return [M2_FIELD_NAMES[c] for c in columns]

def generate_eval_results_csv(qs: QuerySet, fout):
    """
    Generate the CSV of evaluator results that the user downloads when exporting
    the full set of results. When S3_ENABLED == True, this method is used
    by evaluate.py to send the CSV to S3. When S3_ENABLED == False, this
    method is used by views.py to generate the file for the API response.
    """
    writer = csv.writer(fout)
    columns = EvaluatorResultMaterializedView.csv_fields()
    writer.writerow(csv_header_row(columns))
    for i in qs:
        writer.writerow([getattr(i, c) for c in columns])
    return fout

###############
# Utility methods for S3 bucket locations
def full_s3_url(event_id: int, evaluator_id: str, file_ext: str) -> str:
    """
    Generate the full S3 URL where evaluator results files should be saved
    in the S3 bucket. It will follow this format:
    s3://bucket-name/eval_results/event_#/eval-name.json (or csv)

    inputs:
      - event_id: an Event ID (int)
      - evaluator_id: the ID of an evaluator (str)
      - file_ext: "csv" or "json"
    """
    bucket_name = settings.S3_BUCKET_NAME
    bucket_key = s3_bucket_key(event_id, evaluator_id, file_ext)
    return f"s3://{bucket_name}/{bucket_key}"

def s3_bucket_key(event_id: int, evaluator_id: str, file_ext: str):
    """
    Return the file path where an eval results file should live within
    the s3 bucket. Will follow the format:
    eval_results/event_#/eval-name.json (or csv)

    inputs:
      - event_id: an Event ID (int)
      - evaluator_id: the ID of an evaluator (str)
      - file_ext: "csv" or "json"
    """
    filename = s3_filename(evaluator_id, file_ext)
    bucket_directory=f"eval_results/event_{event_id}"
    return f"{bucket_directory}/{filename}"

def s3_filename(evaluator_id: str, file_ext: str):
    """
    Return the filename for an eval results file within the s3 bucket.
    Will follow this format: eval-name.json or eval-name.csv

    inputs:
      - evaluator_id: the ID of an evaluator (str)
      - file_ext: "csv" or "json"
    """
    return f"{evaluator_id}.{file_ext}"
