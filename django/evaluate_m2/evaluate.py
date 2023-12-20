import logging

from evaluate_m2.models import EvaluatorMetaData, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals
from parse_m2.models import Metro2Event


class Evaluate():
    def __init__(self):
        #  When evaluators are provided by additional files, add them here
        #   e.g. self.evaluators = cat7_evals + cat9_evals + ...
        self.evaluators = cat7_evals + cat12_evals + addl_dofd_evals

    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        """
        Given an event, run all evaluators on the Account Activity associated
        to the event and save the results to the database.
        """
        logger = logging.getLogger('evaluate.run_evaluators')

        # run evaluators
        # For this event, all evaluators run on the same set of records
        record_set = event.get_all_account_activity()
        for evaluator in self.evaluators:
            results = evaluator.func(record_set)
            if results:
                # generate evaluator results summary and save before accessed to generate
                # the evaluator results
                result_summary = self.prepare_result_summary(event, evaluator, results)
                result_summary.save()
                evaluator_results = list()
                for row_data in results:
                    result=self.prepare_result(result_summary,
                        row_data)
                    evaluator_results.append(result)
                if (len(evaluator_results) > 0):
                    EvaluatorResult.objects.bulk_create(evaluator_results)

    def prepare_result(self, result_summary: EvaluatorResultSummary,
                       data: dict) -> EvaluatorResult:
        return EvaluatorResult(
            result_summary=result_summary,
            date=data['activity_date'],
            source_record_id=data['id'],
            acct_num=data['cons_acct_num'],
            field_values=data
        )

    def prepare_result_summary(self, event: Metro2Event, evaluator: EvaluatorMetaData,
                               data: list[dict]) -> EvaluatorResultSummary:
        return EvaluatorResultSummary(
            event=event,
            evaluator=evaluator,
            hits=len(data)
        )

# create instance of evaluator
evaluator = Evaluate()
