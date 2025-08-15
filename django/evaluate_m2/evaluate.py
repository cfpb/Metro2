import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.utils.module_loading import import_string

from evaluate_m2.evaluate_utils import  create_eval_insert_query
from evaluate_m2.upload_utils import stream_results_files_to_s3

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary

from parse_m2.models import Metro2Event


class Evaluate():
    # Evaluator version is saved on each evaluator result summary.
    # Increment this version for all updates to evaluator functionality.
    evaluator_version = "1.3"

    def __init__(self):
        self.load_evaluators()

    def load_evaluators(self):
        evaluators_dict = getattr(settings, "METRO2_EVALUATORS", {})
        self.evaluators = {}
        for eval_id, eval_import_str in evaluators_dict.items():
            try:
                eval_callable = import_string(eval_import_str)
            except ImportError:
                raise ImproperlyConfigured(
                    f"Unable to import {eval_import_str} for evaluator "
                    f"{eval_id}. Are you sure the package and evaluator "
                    "callable exist?"
                )
            self.evaluators[eval_id] = eval_callable

    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        """
        Given an event, run all evaluators on the Account Activity associated
        to the event and save the results to the database.
        """
        logger = logging.getLogger('evaluate.run_evaluators')

        record_set = event.get_all_account_activity()
        # run evaluators only if there are records in the record_set
        if record_set.exists():
            for eval_name, eval_func in self.evaluators.items():
                self.run_single_evaluator(event, eval_name, eval_func, record_set)
        else:
            logger.info(f"No AccountActivity found for the event '{event.id}'")

    def run_single_evaluator(self, event, eval_name, eval_func, record_set):
        logger = logging.getLogger('evaluate.run_single_evaluator')
        logger.info(f"Running evaluator: {eval_name}")
        result_summary = self.prepare_result_summary(event, eval_name)
        try:
            self.save_evaluator_results(result_summary, eval_func(record_set))
        except TypeError as e:
            # If the evaluator errors, take note in the eval summary,
            # then continue with the next evaluator
            logger.error(f"Error in evaluator {eval_name}: {e}")
            self.save_error_result(result_summary)
            return

        self.update_result_summary_with_actual_results(result_summary)

        if settings.S3_ENABLED and result_summary.hits > 0:
            stream_results_files_to_s3(result_summary, record_set)


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

    def update_result_summary_with_actual_results(self, result_summary: EvaluatorResultSummary):
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
            result_summary.sample_ids = result_summary.sample_of_results()
            result_summary.save()

    def save_error_result(self, result_summary):
        result_summary.hits = -1
        result_summary.save()

# create instance of evaluator
evaluator = Evaluate()
