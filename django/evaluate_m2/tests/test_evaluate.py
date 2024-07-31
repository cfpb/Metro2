from django.test import TestCase

from datetime import date
from evaluate_m2.evaluate import evaluator
from evaluate_m2.m2_evaluators.status_evals import (
    eval_status_dofd_1_func,
    eval_status_dofd_2_func)
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import M2DataFile, Metro2Event
from evaluate_m2.tests.evaluator_test_helper import acct_record


def sample_eval_always_hits(record_set):
    return record_set

def sample_eval_never_hits(record_set):
    return record_set.filter(cons_acct_num="bogus")

def sample_erroring_eval(record_set):
    return EvaluatorMetadata.objects.filter(rationale='thing')

class EvaluateTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event.objects.create(name='test_exam')
        self.data_file = M2DataFile.objects.create(event=self.event, file_name='file.txt')
        # Create AccountActivity records
        # activity_date defaults to 2022-05-30
        acct_record(self.data_file, {'id': 44, 'cons_acct_num': '1044'})
        acct_record(self.data_file, {'id': 45, 'cons_acct_num': '1045'})
        acct_record(self.data_file, {'id': 46, 'cons_acct_num': '1046'})
        acct_record(self.data_file, {'id': 47, 'cons_acct_num': '1047'})

    def test_run_evaluators_no_evals(self):
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = {}
        evaluator.run_evaluators(self.event)

        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        self.assertEqual(0, EvaluatorResult.objects.count())
        self.assertEqual(0, EvaluatorResultSummary.objects.count())
        self.assertEqual(0, EvaluatorMetadata.objects.count())

    def test_run_evaluators_produces_correct_results(self):
        evaluator.evaluators = {"Sample-1": sample_eval_always_hits}
        evaluator.run_evaluators(self.event)

        self.assertEqual(4, EvaluatorResult.objects.count())
        self.assertEqual(1, EvaluatorResultSummary.objects.count())

        # Creates correct EvaluatorResult records
        results = EvaluatorResultSummary.objects.get(event=self.event, evaluator__id='Sample-1') \
            .evaluatorresult_set.order_by('acct_num')

        # Test that results match AccountActivity records for the event
        self.assertEqual(results[0].source_record_id, 44)
        self.assertEqual(results[1].source_record_id, 45)
        self.assertEqual(results[2].source_record_id, 46)
        self.assertEqual(results[3].source_record_id, 47)

        self.assertEqual(results[0].acct_num, '1044')
        self.assertEqual(results[1].acct_num, '1045')
        self.assertEqual(results[2].acct_num, '1046')
        self.assertEqual(results[3].acct_num, '1047')

    def test_run_evaluators_with_two_evaluators_produces_results(self):
        evaluator.evaluators = {"Sample-1": sample_eval_always_hits,
                                "Sample-2": sample_eval_never_hits}
        evaluator.run_evaluators(self.event)
        self.assertEqual(2, EvaluatorResultSummary.objects.count())

        # evaluator creates EvaluatorMetadata object for Sample-1
        eval1 = EvaluatorMetadata.objects.get(id="Sample-1")
        summary1 = eval1.evaluatorresultsummary_set.first()
        # actual number of hits matches EvaluatorResultSummary.hits
        self.assertEqual(4, summary1.hits)
        self.assertEqual(4, summary1.evaluatorresult_set.count())

        # evaluator creates EvaluatorMetadata object for Sample-2
        eval2 = EvaluatorMetadata.objects.get(id="Sample-2")
        summary2 = eval2.evaluatorresultsummary_set.first()
        # actual number of hits matches EvaluatorResultSummary.hits
        self.assertEqual(0, summary2.hits)
        self.assertEqual(0, summary2.evaluatorresult_set.count())

    def test_eval_summary_gets_updated_with_actual_results(self):
        act_date = date(2022, 5, 30)
        evaluator.evaluators = {"Sample-1": sample_eval_always_hits}
        evaluator.run_evaluators(self.event)
        result_summary = EvaluatorResultSummary.objects.get(event=self.event, evaluator__id='Sample-1')
        self.assertEqual(result_summary.hits, 4)
        self.assertEqual(result_summary.accounts_affected, 4)
        self.assertEqual(result_summary.inconsistency_start, act_date)
        self.assertEqual(result_summary.inconsistency_end, act_date)

    def test_run_evaluators_with_no_records_does_not_raise_exception(self):
        event = Metro2Event.objects.create(name='test_no_activity_exam')
        evaluator.evaluators = {"Status-DOFD-1": eval_status_dofd_1_func,
                                "Status-DOFD-2": eval_status_dofd_2_func}
        evaluator.run_evaluators(event)

        self.assertEqual(0, EvaluatorResult.objects.count())
        self.assertEqual(0, EvaluatorResultSummary.objects.count())
        self.assertEqual(0, EvaluatorMetadata.objects.count())

    def test_erroring_eval_gets_skipped(self):
        evaluator.evaluators = {"Sample-err": sample_erroring_eval,
                                "Sample-1": sample_eval_always_hits,}
        evaluator.run_evaluators(self.event)

        eval2 = EvaluatorMetadata.objects.get(id="Sample-err")
        summary2 = eval2.evaluatorresultsummary_set.first()
        # errored evals get hits = -1
        self.assertEqual(-1, summary2.hits)

        # Other evals still run after the error
        eval1 = EvaluatorMetadata.objects.get(id="Sample-1")
        summary1 = eval1.evaluatorresultsummary_set.first()
        self.assertEqual(4, summary1.hits)
