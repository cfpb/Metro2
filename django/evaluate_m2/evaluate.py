import logging

from evaluate_m2.evaluate_utils import get_activity_date_range_from_list
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.m2_evaluators.account_change_evals import evaluators as acct_change_evals
from evaluate_m2.m2_evaluators.balance_evals import evaluators as balance_evals
from evaluate_m2.m2_evaluators.balloon_evals import evaluators as balloon_evals
from evaluate_m2.m2_evaluators.bankruptcy_evals import evaluators as bankruptcy_evals
from evaluate_m2.m2_evaluators.ccc_evals import evaluators as ccc_evals
from evaluate_m2.m2_evaluators.deferred_evals import evaluators as deferred_evals
from evaluate_m2.m2_evaluators.doai_evals import evaluators as doai_evals
from evaluate_m2.m2_evaluators.dtcl_evals import evaluators as dtcl_evals
from evaluate_m2.m2_evaluators.prog_evals import evaluators as prog_evals
from evaluate_m2.m2_evaluators.rating_evals import evaluators as rating_evals
from evaluate_m2.m2_evaluators.scc_evals import evaluators as scc_evals
from evaluate_m2.m2_evaluators.status_evals import evaluators as status_evals
from evaluate_m2.m2_evaluators.type_evals import evaluators as type_evals
from parse_m2.models import Metro2Event


class Evaluate():
    def __init__(self):
        self.evaluators = acct_change_evals | balance_evals | balloon_evals | \
                          bankruptcy_evals | ccc_evals | deferred_evals | \
                          doai_evals | dtcl_evals | rating_evals | prog_evals | \
                          scc_evals | status_evals | type_evals


    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        """
        Given an event, run all evaluators on the Account Activity associated
        to the event and save the results to the database.
        """
        logger = logging.getLogger('evaluate.run_evaluators')  # noqa: F841

        record_set = event.get_all_account_activity()
        # run evaluators only if there are records in the record_set
        if record_set:
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
        else:
            logger.info(f"No AccountActivity found for the event '{event.name}'")

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
        accounts_affected = list(set(d['cons_acct_num'] for d in data))
        date_range = get_activity_date_range_from_list(data)
        try:
            eval_metadata = EvaluatorMetadata.objects.get(id=eval_id)
        except EvaluatorMetadata.DoesNotExist:
            eval_metadata = EvaluatorMetadata.objects.create(id=eval_id)

        return EvaluatorResultSummary.objects.create(
            event=event,
            evaluator=eval_metadata,
            hits=len(data),
            accounts_affected = len(accounts_affected),
            inconsistency_start = date_range["earliest"],
            inconsistency_end = date_range["latest"]
        )

# create instance of evaluator
evaluator = Evaluate()
