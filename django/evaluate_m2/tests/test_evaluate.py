
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from datetime import datetime
from evaluate_m2.evaluate import evaluator
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from evaluate_m2.models import EvaluatorMetaData, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper

from parse_m2.models import K2, AccountActivity, M2DataFile, Metro2Event


class TestEvaluate(TestCase, EvaluatorTestHelper):
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
            'cons_acct_num': '0032', 'spc_com_cd': 'C', 'acct_stat': '71',
            'amt_past_due': 0, 'current_bal': 0, 'date_closed': datetime(2020, 1, 1).date(),
            'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0033', 'spc_com_cd': 'AX', 'acct_stat': '11',
            'amt_past_due': 9, 'current_bal': 9, 'date_closed': datetime(2020, 1, 1).date(),
            'k2__purch_sold_ind': None
        }]
        self.unexpected = {
            'id': 36, 'activity_date': datetime(2019, 12, 31).date(),
            'cons_acct_num': '0036', 'spc_com_cd': 'AX', 'acct_stat': '11',
            'amt_past_due': 9, 'current_bal': 9, 'date_closed': datetime(2020, 1, 1).date(), 'k2__purch_sold_ind': None
        }

        # Need to reset to an empty list after each test
        evaluator.evaluators = cat7_evals
        evaluator.metadata = list()
        evaluator.evaluator_results = list()

    def create_k2_segments(self):
        # Create the segment data
        k2_data = {'id':(32,34,35), 'purch_sold_ind':('a','b','c'),
                   'purch_sold_name':('hit','no1','no2')}
        self.k2 = self.create_bulk_k2(k2_data, 3)

    def create_other_segments(self):
        # Create the segment data
        self.j1 = self.create_jsegment(32, 'j1', 'a1')
        self.j1.save()
        self.j2 = self.create_jsegment(32, 'j2', 'a2')
        self.j2.save()
        self.l1 = self.create_l1(32)
        self.l1.save()

    def create_data(self, activities, size):
        self.account_activity = self.create_bulk_activities(self.data_file,
            activities, size)
        # Create the segment data
        self.create_k2_segments()

    ############################
    # Tests for the evaluate
    def test_run_evaluators_no_evals(self):
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators(self.event)

        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        expected = list()
        self.assertListEqual(expected, evaluator.evaluator_results)
        self.assertListEqual(expected, evaluator.metadata)

    def test_run_evaluators_produces_results(self):
        # should correctly insert one statement and one metadata statement
        # Account Activity data
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-acct_stat=65
        self.create_data(activities, 4)

        evaluator.evaluators = [cat7_evals[0]]
        evaluator.run_evaluators(self.event)
        self.assertEqual(2, len(evaluator.evaluator_results))
        self.assertEqual(1, len(evaluator.metadata))

    def test_run_evaluators_with_two_evaluators_produces_results(self):
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','61','62'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,10,20,30),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: Evaluator1 - HIT, 2: Evaluator1 & Evaluator2 - HIT,
        # 3: NO HIT 4: Evaluator2 - HIT

        self.create_data(activities, 4)

        evaluator.evaluators=cat7_evals[:2]
        evaluator.run_evaluators(self.event)
        self.assertEqual(4, len(evaluator.evaluator_results))
        self.assertEqual(2, len(evaluator.metadata))

        # first evaluator metadata and results
        self.assertEqual(evaluator.evaluators[0].name,
            evaluator.metadata[0].name)
        self.assertEqual(2, EvaluatorResultSummary.objects.get(evaluator=evaluator.metadata[0]).hits)
        self.assertEqual(2, EvaluatorResult.objects.filter(
            result_summary=EvaluatorResultSummary.objects.get(
                id=evaluator.evaluators[0].id)).count())

        # second evaluator metadata and results
        self.assertEqual(evaluator.evaluators[1].name,
            evaluator.metadata[1].name)
        self.assertEqual(2, EvaluatorResultSummary.objects.get(evaluator=evaluator.metadata[1]).hits)
        self.assertEqual(2, EvaluatorResult.objects.filter(
            result_summary=EvaluatorResultSummary.objects.get(
                id=evaluator.evaluators[1].id)).count())

    def test_prepare_results_creates_an_object(self):
        # should correctly create one EvaluatorResult object
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AU','WT','AU')}
        # 1: HIT, 2: NO-spc_com_cd=AU, 3: NO-spc_com_cd=WT, 4: NO-acct_stat=65
        self.create_data(activities, 4)

        evl = cat7_evals[0]
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
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-acct_stat=65
        self.create_data(activities, 4)

        evl = cat7_evals[0]
        evl.save()
        return_value = evaluator.prepare_result_summary(self.event, evl, self.expected)

        self.assertEqual( evl.name, return_value.evaluator.name)
        self.assertEqual( 2, return_value.hits)

    def test_run_evaluators_invalid_source_record_raises_exception(self):
        # should raise an exception when the source_record does not exist
        evl =EvaluatorMetaData(name='Test')
        evl.set_func(func=self.set_mock_function)
        evaluator.evaluators = [evl]

        with self.assertRaises(ObjectDoesNotExist) as cm:
            evaluator.run_evaluators(Metro2Event.objects.get(name=self.event.name))
        self.assertEqual(cm.exception.args[0], 'AccountActivity matching query does not exist.')

    def test_prepare_results_invalid_evaluator_raises_exception(self):
        # should raise an exception when the evaluator does not exist
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-acct_stat=65
        self.create_data(activities, 4)

        evl = cat7_evals[0]

        with self.assertRaises(ObjectDoesNotExist) as cm:
            evaluator.prepare_result_summary(self.event, evl, self.account_activity[0])
        self.assertEqual(cm.exception.args[0], 'EvaluatorMetaData matching query does not exist.')

    def test_run_evaluators_missing_parameter_raises_exception(self):
        # should raise an exception when the source_record does not exist
        evl =EvaluatorMetaData(name='Test')
        evl.set_func(func=self.set_mock_function)
        evaluator.evaluators = [evl]

        with self.assertRaises(TypeError) as cm:
            evaluator.run_evaluators()
        self.assertEqual(cm.exception.args[0], "Evaluate.run_evaluators() missing 1 required positional argument: 'event'")
    def set_mock_function(self):
        return [self.unexpected]
