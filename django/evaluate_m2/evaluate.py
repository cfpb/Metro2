import csv
import json
import logging

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection

from django_application.s3_utils import s3_session
from evaluate_m2.evaluate_utils import (
    create_eval_insert_query,
    get_randomizer,
    get_url
)
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary
from evaluate_m2.m2_evaluators.account_change_evals import evaluators as acct_change_evals
from evaluate_m2.m2_evaluators.balance_evals import evaluators as balance_evals
from evaluate_m2.m2_evaluators.balloon_evals import evaluators as balloon_evals
from evaluate_m2.m2_evaluators.bankruptcy_evals import evaluators as bankruptcy_evals
from evaluate_m2.m2_evaluators.ccc_evals import evaluators as ccc_evals
from evaluate_m2.m2_evaluators.deferred_evals import evaluators as deferred_evals
from evaluate_m2.m2_evaluators.doai_evals import evaluators as doai_evals
from evaluate_m2.m2_evaluators.dtcl_evals import evaluators as dtcl_evals
from evaluate_m2.m2_evaluators.ecoa_evals import evaluators as ecoa_evals
from evaluate_m2.m2_evaluators.php_evals import evaluators as php_evals
from evaluate_m2.m2_evaluators.prog_evals import evaluators as prog_evals
from evaluate_m2.m2_evaluators.rating_evals import evaluators as rating_evals
from evaluate_m2.m2_evaluators.scc_evals import evaluators as scc_evals
from evaluate_m2.m2_evaluators.status_evals import evaluators as status_evals
from evaluate_m2.m2_evaluators.type_evals import evaluators as type_evals

from parse_m2.models import Metro2Event
from smart_open import open


class Evaluate():
    # Evaluator version is saved on each evaluator result summary.
    # Increment this version for all updates to evaluator functionality.
    evaluator_version = "1.1"

    def __init__(self):
        self.evaluators = acct_change_evals |  balance_evals | balloon_evals | \
                          bankruptcy_evals | ccc_evals | deferred_evals | \
                          doai_evals | dtcl_evals | ecoa_evals | php_evals | \
                          prog_evals | rating_evals | scc_evals | status_evals | \
                          type_evals

    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        """
        Given an event, run all evaluators on the Account Activity associated
        to the event and save the results to the database.
        """
        logger = logging.getLogger('evaluate.run_evaluators')  # noqa: F841

        if settings.SSO_ENABLED:
            bucket_name = settings.S3_BUCKET_NAME
        record_set = event.get_all_account_activity()
        # run evaluators only if there are records in the record_set
        if record_set.exists():
            for eval_name, func in self.evaluators.items():
                logger.info(f"Running evaluator: {eval_name}")
                result_summary = self.prepare_result_summary(event, eval_name)
                try:
                    self.save_evaluator_results(result_summary, func(record_set))
                except TypeError as e:
                    # If the evaluator errors, take note in the eval summary,
                    # then continue with the next evaluator
                    logger.error(f"Error in evaluator {eval_name}: {e}")
                    self.save_error_result(result_summary)
                    continue
                self.update_result_summary_with_actual_results(result_summary)
                if settings.S3_ENABLED:
                    self.stream_eval_result_files_to_s3(result_summary, record_set, bucket_name)
        else:
            logger.info(f"No AccountActivity found for the event '{event.name}'")

    def stream_eval_result_files_to_s3(self, result_summary, record_set, bucket_name):
        """
        If the EvaluatorResultSummary record has accounts affected,
        save the evaluator results files to an S3 bucket.
        """
        logger = logging.getLogger('evaluate.stream_eval_result_files_to_s3')  # noqa: F841
        RESULTS_PAGE_SIZE = 20
        CHUNK_SIZE = 25000

        # Only create files if there are hits
        if result_summary.hits > 0:
            url = get_url(str(result_summary.event.id),result_summary.evaluator.id)
            total_hits = min(result_summary.hits, 1_000_000)

            fields_list = result_summary.evaluator.result_summary_fields()
            randomizer = get_randomizer(total_hits, RESULTS_PAGE_SIZE)
            sample_id_list = []
            # TODO: Maximum row size for files should be a million rows
            with open(f"{url}.csv", 'w', transport_params={'client': s3_session()}) as fout:
                writer = csv.writer(fout)
                # Add the header to the CSV response
                writer.writerow(result_summary.create_csv_header())
                for i in range(0, total_hits, CHUNK_SIZE):
                    max_count = min(total_hits, (i + CHUNK_SIZE))
                    logger.debug(f"\tGetting chunk size: [{i}: {max_count}]")
                    for idx, eval_result in enumerate(result_summary.evaluatorresult_set.all()[i:max_count], start=i):
                        if idx % randomizer == 0 and len(sample_id_list) < RESULTS_PAGE_SIZE:
                            sample_id_list.append(eval_result.source_record_id)
                        writer.writerow(eval_result.create_csv_row_data(fields_list))
            logger.info(f"Completed saving file at: {url}.csv")

            logger.info(f"Saving file at: {url}.json")
            self.save_evaluator_results_json_to_s3(record_set, fields_list, sample_id_list, url)
            logger.info(f"Completed saving file at: {url}.json")

    def save_evaluator_results_json_to_s3(self, record_set, fields_list, id_list, url):
        """
        Save a sample of evaluator results JSON to an S3 bucket.
        """
        with open(f"{url}.json", 'w', transport_params={'client': s3_session()}) as jsonFile:
            result = record_set.filter(id__in=id_list) \
                .values(*fields_list)
            response = {'hits': [obj for obj in result]}
            json.dump(response, jsonFile, cls=DjangoJSONEncoder)

    def save_evaluator_results(self, result_summary, eval_query):
        """
        Use a raw SQL query to run the evaluator and save the results
        to the EvaluatorResult table.
        """
        select_query, query_params = eval_query.query.sql_with_params()

        full_query = create_eval_insert_query(select_query, result_summary)

        with connection.cursor() as cursor:
            cursor.execute(full_query, query_params)

    def prepare_result_summary(self, event: Metro2Event, eval_id: str) -> EvaluatorResultSummary:
        """
        Create an EvaluatorResultSummary object so we can associate results with it.
        Later, we will update the values related to eval hits.
        """
        # If an EvaluatorMetadata record already exists in the database with this name,
        # associate the results with that record. If one does not exist, create it.
        try:
            eval_metadata = EvaluatorMetadata.objects.get(id=eval_id)
        except EvaluatorMetadata.DoesNotExist:
            eval_metadata = EvaluatorMetadata.objects.create(id=eval_id)

        return EvaluatorResultSummary.objects.create(
            event = event,
            evaluator = eval_metadata,
            hits = 0,
            accounts_affected = 0,
            evaluator_version = self.evaluator_version,
        )

    def update_result_summary_with_actual_results(self, result_summary):
        """
        If the evaluator had any hits, update the information about the hits
        in the EvaluatorResultSummary record.
        """
        data = result_summary.evaluatorresult_set
        if data.exists():
            hits = data.count()
            accounts_affected = data.values('acct_num').distinct().count()
            earliest_date = data.order_by('date').first().date
            latest_date = data.order_by('-date').first().date

            result_summary.hits = hits
            result_summary.accounts_affected = accounts_affected
            result_summary.inconsistency_start = earliest_date
            result_summary.inconsistency_end = latest_date
            result_summary.save()

    def save_error_result(self, result_summary):
        result_summary.hits = -1
        result_summary.save()

# create instance of evaluator
evaluator = Evaluate()
