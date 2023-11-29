import sys
import logging
from parse_m2.models import AccountActivity
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult
from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals

class Evaluate():
    def __init__(self):
        #  When evaluators are provided by additional files, add them here
        #   e.g. self.evaluators = cat7_evals + cat9_evals + ...
        self.evaluators = addl_dofd_evals + cat7_evals + cat12_evals
        self.date_format = '%m%d%Y'

    # runs evaluators to produce results
    def run_evaluators(self):
        logger = logging.getLogger('evaluate.run_evaluators')

        # run evaluators
        for evaluator in self.evaluators:
            results = evaluator.exec_custom_func()
            # Generate results and metadata objects to be saved
            if results:
                evaluatorResult = list()
                try:
                    # generate evaluator metadata
                    self.metadata = self.prepare_metadata(evaluator, results)
                    self.metadata.save()
                    for row_data in results:
                        # prepare results
                        evaluatorResult.append(self.prepare_result_data(evaluator, row_data))

                    EvaluatorResult.objects.bulk_create(evaluatorResult)
                except KeyError as e:
                    logger.error(f"Unable to add result to results: {e}")
                    # this should only be raised by a developer error
                    # so we want to exit.
                    sys.exit(1)

    def prepare_results(self, evaluator, data):
        return EvaluatorResult(
            evaluator=EvaluatorMetadata.objects.get(evaluator_name=evaluator.name),
            date=data['activity_date'],
            source_record=AccountActivity.objects.get(id=data['id']),
            acct_num=data['cons_acct_num'],
            field_values=data
        )

    def prepare_metadata(self, evaluator, data):
        return EvaluatorMetadata(
            evaluator_name=evaluator.name,
            hits=len(data)
        )

# create instance of evaluator
evaluator = Evaluate()
