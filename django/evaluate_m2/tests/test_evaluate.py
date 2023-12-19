from django.test import TestCase

from datetime import datetime
from evaluate_m2.evaluate import evaluator
from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd
from evaluate_m2.models import EvaluatorMetaData, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import AccountActivity, M2DataFile, Metro2Event


class EvaluateTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W'))
        self.expected = [{
            'id': 32, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0032', 'acct_stat': '71', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(), 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
        }, {
            'id': 33, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0033', 'acct_stat': '97', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(), 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
        }]
        self.unexpected = {
            'id': 36, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0036', 'acct_stat': '71', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':'0', 'current_bal': 0,
            'date_closed': datetime(2020, 1, 1).date(), 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': 'X', 'terms_freq': '0'
        }

        # Need to reset to an empty list after each test
        evaluator.evaluators = addl_dofd

    def create_data(self, activities, size):
        self.account_activity = self.create_bulk_activities(self.data_file,
            activities, size)

    ############################
    # Tests for evaluate
    def test_run_evaluators_no_evals(self):
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators(self.event)

        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        self.assertEqual(0, EvaluatorResult.objects.count())
        self.assertEqual(0, EvaluatorResultSummary.objects.count())
        self.assertEqual(0, EvaluatorMetaData.objects.count())

    def test_run_evaluators_produces_results(self):
        # should correctly insert one statement and one metadata statement
        # Account Activity data
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'),
            'acct_stat':('71','97','11','65'),
            'dofd':(None,None,None,datetime(2019, 12, 31))}
        # 1: HIT, 2: HIT, 3: NO-acct_stat=11, 4: NO-dofd=01012020
        self.create_data(activities, 4)

        evaluator.evaluators = [addl_dofd[0]]
        evaluator.run_evaluators(self.event)

        self.assertEqual(2, EvaluatorResult.objects.count())
        self.assertEqual(1, EvaluatorResultSummary.objects.count())
        self.assertEqual(1, EvaluatorMetaData.objects.count())

    def test_run_evaluators_with_two_evaluators_produces_results(self):
        activities = { 'id':(32,33,34,35),
            'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'),
            'acct_stat':('71','13','11','97'),
            'dofd':(None,None,datetime(2019, 12, 31),None),
            'pmt_rating':('1','2','0','L')}
        # 1: Evaluator1 - HIT, 2: Evaluator2 - HIT,
        # 3: NO HIT 4: Evaluator1 - HIT

        self.create_data(activities, 4)

        evaluator.evaluators=addl_dofd[:2]
        evaluator.run_evaluators(self.event)
        self.assertEqual(2, EvaluatorResultSummary.objects.count())
        self.assertEqual(2, EvaluatorMetaData.objects.count())

        # first evaluator metadata and results
        self.assertEqual(2, EvaluatorResultSummary.objects.get(
            evaluator=evaluator.evaluators[0]).hits)
        self.assertEqual(2, EvaluatorResult.objects.filter(
            result_summary=EvaluatorResultSummary.objects.get(
                id=evaluator.evaluators[0].id)).count())

        # second evaluator metadata and results
        self.assertEqual(1, EvaluatorResultSummary.objects.get(
            evaluator=evaluator.evaluators[1]).hits)
        self.assertEqual(1, EvaluatorResult.objects.filter(
            result_summary=EvaluatorResultSummary.objects.get(
                id=evaluator.evaluators[1].id)).count())

    def test_prepare_results_creates_an_object(self):
        # should correctly create one EvaluatorResult object
        activities = { 'id':(32,33,34), 'cons_acct_num':('0032','0033','0034'),
            'account_holder':('Z','Y','X'),
            'acct_stat':('71','66','65'),
            'dofd':(None,None,datetime(2019, 12, 31))}
        # 1: HIT, 2: NO-acct_stat=66, 3: NO-acct_stat=11, 4: NO-dofd=01012020

        self.create_data(activities, 3)

        evl = addl_dofd[0]
        evl.save()
        result_summary = evaluator.prepare_result_summary(self.event, evl, self.expected)
        result_summary.save()
        return_value = evaluator.prepare_result(result_summary, self.expected[0])

        self.assertEqual(EvaluatorMetaData.objects.get(name=evl.name),
                         return_value.result_summary.evaluator)
        self.assertEqual(self.expected[0]['activity_date'], return_value.date)
        self.assertEqual(AccountActivity.objects.get(id=self.expected[0]['id']),
                         return_value.source_record)
        self.assertEqual(self.expected[0]['cons_acct_num'], return_value.acct_num)
        self.assertEqual(self.expected[0], return_value.field_values)

    def test_prepare_result_summary_creates_an_object(self):
        # should correctly create one EvaluatorMetaData object
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'),
            'acct_stat':('71','97','11','65'),
            'dofd':(None,None,None,datetime(2019, 12, 31))}
        # 1: HIT, 2: HIT, 3: NO-acct_stat=11, 4: NO-dofd=01012020
        self.create_data(activities, 4)

        evl = addl_dofd[0]
        evl.save()
        return_value = evaluator.prepare_result_summary(self.event, evl, self.expected)

        self.assertEqual( evl.name, return_value.evaluator.name)
        self.assertEqual( 2, return_value.hits)

    def test_run_evaluators_missing_parameter_raises_exception(self):
        # should raise an exception when the source_record does not exist
        evl =EvaluatorMetaData(name='Test')
        evl.set_func(func=self.set_mock_function)
        evaluator.evaluators = [evl]

        with self.assertRaises(TypeError) as cm:
            evaluator.run_evaluators()
        self.assertEqual(cm.exception.args[0], "Evaluate.run_evaluators() missing 1 required positional argument: 'event'")

    def set_mock_function(self, mock_set):
        return [self.unexpected]
