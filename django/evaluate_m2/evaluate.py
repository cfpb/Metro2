import sys
import logging
from evaluate_m2.models import EvaluatorMetaData, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals
from parse_m2.models import AccountActivity, Metro2Event


class Evaluate():
    def __init__(self):
        #  When evaluators are provided by additional files, add them here
        #   e.g. self.evaluators = cat7_evals + cat9_evals + ...
        self.evaluators = cat7_evals + cat12_evals + addl_dofd_evals
        self.date_format = '%m%d%Y'
        self.evaluator_results = list()
        self.evaluator_results_summary = list()
        self.metadata = list()

    # runs evaluators to produce results
    def run_evaluators(self, event: Metro2Event):
        logger = logging.getLogger('evaluate.run_evaluators')
        # run evaluators
        # For this event, all evaluators run on the same set of records
        record_set = event.get_all_account_activity()
        for evaluator in self.evaluators:
            self.metadata.append(evaluator)
            # Generate evaluator metadata and save before accessed to generate
            # the evaluator results summary
            evaluator.set_metro2_event(event=event.name)
            evaluator.save()
            results = evaluator.func(record_set)
            if results:
                # generate evaluator results summary and save before accessed to generate
                # the evaluator results
                result_summary = self.prepare_result_summary(event, evaluator, results)
                self.evaluator_results_summary.append(result_summary)
                result_summary.save()

                for row_data in results:
                    result=self.prepare_result(result_summary,
                        row_data)
                    self.evaluator_results.append(result)

        if (len(self.evaluator_results) > 0):
            EvaluatorResult.objects.bulk_create(self.evaluator_results)

    def prepare_result(self, result_summary: EvaluatorResultSummary,
                       data: dict) -> EvaluatorResult:
        return EvaluatorResult(
            # At the moment, this is not a problem, but in the future with many exams,
            # there is nothing differentiating one EvaluatorMetaData from another since
            # the name is not unique
            result_summary=EvaluatorResultSummary.objects.get(
                evaluator=result_summary.evaluator.id),
            date=data['activity_date'],
            source_record=AccountActivity.objects.get(id=data['id']),
            acct_num=data['cons_acct_num'],
            field_values=data
        )

    def prepare_result_summary(self, event: Metro2Event, evaluator: EvaluatorMetaData,
                               data: list[dict]) -> EvaluatorResultSummary:
        return EvaluatorResultSummary(
            event=event,
            evaluator=EvaluatorMetaData.objects.get(id=evaluator.id),
            hits=len(data)
        )

# create instance of evaluator
evaluator = Evaluate()
