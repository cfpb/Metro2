import logging
import csv
import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django_application.s3_utils import s3_session

from smart_open import open

from evaluate_m2.models import EvaluatorResultSummary

def stream_results_files_to_s3(result_summary: EvaluatorResultSummary, record_set):
    stream_full_results_csv_to_s3(result_summary)
    stream_sample_results_json_to_s3(result_summary, record_set)

##############
# Methods for generating and uploading full CSV
def stream_full_results_csv_to_s3(result_summary: EvaluatorResultSummary, url: str = None):
    """
    If the EvaluatorResultSummary record has accounts affected,
    save the evaluator results files to an S3 bucket.
    """
    logger = logging.getLogger('evaluate.stream_full_results_csv_to_s3')
    if not url:
        url = full_s3_url(result_summary.event_id, result_summary.evaluator_id, 'csv')
    logger.info(f"Saving CSV at: {url}")

    with open(url, 'w', transport_params={'client': s3_session()}) as fout:
        generate_full_csv(result_summary, fout)
    logger.debug("Completed saving CSV file")

def generate_full_csv(result_summary: EvaluatorResultSummary, fout):
    """
    Generate the CSV of evaluator results that the user downloads when exporting
    the full set of results. When S3_ENABLED == True, this method is used
    by evaluate.py to send the CSV to S3. When S3_ENABLED == False, this
    method is used by views.py to generate the file for the API response.
    """
    logger = logging.getLogger('evaluate.generate_full_csv')

    # For now, limit file uploads to 1 million records
    # TODO: handle uploading results where hits > 1 million
    total_hits = min(result_summary.hits, 1_000_000)
    CHUNK_SIZE = 25000
    fields_list = result_summary.evaluator.result_summary_fields()

    writer = csv.writer(fout)
    # Add the header to the CSV response
    writer.writerow(result_summary.create_csv_header())
    for i in range(0, total_hits, CHUNK_SIZE):
        max_count = min(total_hits, (i + CHUNK_SIZE))
        logger.debug(f"\tGetting chunk size: [{i}: {max_count}]")
        for eval_result in result_summary.evaluatorresult_set.all()[i:max_count]:
            # TODO: This method queries the database for every eval result.
            # Find a way to use pre-fetched data to improve efficiency
            writer.writerow(eval_result.create_csv_row_data(fields_list))

    return fout


##############
# Methods for generating and uploading JSON sample
def stream_sample_results_json_to_s3(result_summary: EvaluatorResultSummary, record_set, url: str = None):
    """
    Save the set of sample of evaluator results as JSON to an S3 bucket.
    """
    logger = logging.getLogger('evaluate.stream_sample_results_json_to_s3')
    if not url:
        url = full_s3_url(result_summary.event_id, result_summary.evaluator_id, 'json')
    logger.info(f"Saving JSON file at: {url}")

    with open(url, 'w', transport_params={'client': s3_session()}) as jsonFile:
        response = generate_json_sample(result_summary, record_set)
        json.dump(response, jsonFile, cls=DjangoJSONEncoder)
    logger.debug("Completed saving JSON file")

# TODO: Combine this with and/or use the
# EvaluatorResultAccountActivitySerializer for serializing the resulting
# records.
def generate_json_sample(result_summary: EvaluatorResultSummary, record_set):
    """
    Generate the JSON of evaluator results that is sent to the front-end
    on the evaluator results view. When S3_ENABLED == True, this method is used
    by evaluate.py to send the JSON to S3. When S3_ENABLED == False, this
    method is used by views.py to generate the JSON for the API response.

    The set of results is the set of AccountActivity records specified by
    result_summary.sample_ids. This value should be populated during the
    evaluate process (in update_result_summary_with_actual_results).
    If not, as a fallback, just return the first 20 AccountActivity records.
    """
    fields_list = result_summary.evaluator.result_summary_fields()
    sample_ids = result_summary.sample_ids

    if not sample_ids or (len(sample_ids) == 0):
        page_size = settings.M2_RESULT_SAMPLE_SIZE
        records = record_set \
            .order_by('activity_date') \
            .values(*fields_list)[:page_size]
    else:
        records = record_set.filter(id__in=sample_ids) \
        .order_by('activity_date') \
        .values(*fields_list)
    return {'hits': [obj for obj in records]}


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
