import logging

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.m2_evaluators.addl_bk_evals import evaluators as addl_bk_evals
from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from evaluate_m2.m2_evaluators.cat9_evals import evaluators as cat9_evals
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals
from parse_m2.models import Metro2Event


class Evaluate():
    def __init__(self):
        #  When evaluators are provided by additional files, add them here
        #   e.g. self.evaluators = cat7_evals | cat9_evals | ...
        self.evaluators = addl_bk_evals | addl_dofd_evals | cat7_evals | \
                          cat9_evals | cat12_evals

    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        """
        Given an event, run all evaluators on the Account Activity associated
        to the event and save the results to the database.
        """
        logger = logging.getLogger('evaluate.run_evaluators')  # noqa: F841

        record_set = event.get_all_account_activity()
        # run evaluators
        for eval_name, func in self.evaluators.items():
            logger.info(f"Running evaluator: {eval_name}")
            results = func(record_set)
            if results:
                # generate evaluator results summary and save before accessed to generate
                # the evaluator results
                result_summary = self.prepare_result_summary(event, eval_name, results)
                evaluator_results = list()
                for row_data in results:
                    result=self.prepare_result(result_summary, row_data)
                    evaluator_results.append(result)
                if (len(evaluator_results) > 0):
                    EvaluatorResult.objects.bulk_create(evaluator_results)
                    logger.info(f"Evaluator results written to the database: {len(evaluator_results)}")

    def prepare_result(self, result_summary: EvaluatorResultSummary,
                       data: dict) -> EvaluatorResult:
        return EvaluatorResult(
            result_summary=result_summary,
            date=data['activity_date'],
            source_record_id=data['id'],
            acct_num=data['cons_acct_num'],
            field_values=data
        )

    def prepare_result_summary(self, event: Metro2Event, eval_id: str,
                               data: list[dict]) -> EvaluatorResultSummary:
        """
        If an EvaluatorMetadata record already exists in the database with this name,
        associate the results with that record. If one does not exist, create it.

        Ideally, every evaluator function should already have an associated EvalMetadata
        record, so the "except" clause here is just a failsafe in case we messed up
        the Metadata import.
        """
        try:
            eval_metadata = EvaluatorMetadata.objects.get(id=eval_id)
        except EvaluatorMetadata.DoesNotExist:
            eval_metadata = EvaluatorMetadata.objects.create(id=eval_id)

        return EvaluatorResultSummary.objects.create(
            event=event,
            evaluator=eval_metadata,
            hits=len(data)
        )

# create instance of evaluator
evaluator = Evaluate()
