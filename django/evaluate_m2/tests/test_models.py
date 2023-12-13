from django.test import TestCase

from evaluate_m2.models import EvaluatorMetaData
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import M2DataFile, Metro2Event


class Cat7_EvalsTestCase(TestCase, EvaluatorTestHelper):


    def create_exam_activity(self):
        # Create the Account Activities data
        activities = {'id':(34,35),  'account_holder':('X','W'),
                      'acct_type':('12','91'), 'cons_acct_num':('0034','0035'), 'credit_limit':(30,40), 'hcola':(-5,-5), 'port_type':('I','I'),
                      'terms_dur':('15','20'), 'terms_freq':('P','D')}
        # Create the parent records for the AccountActivity data for first event
        event = Metro2Event(name='test_exam')
        event.save()
        self.file = M2DataFile(event=event, file_name='file.txt')
        self.file.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.file, ('X','W'))
        self.account_activity = self.create_bulk_activities(self.file, activities, 2)

        # Create the second exam Account Activities data
        activities2 = {'id':(32,33),
                      'account_holder':('Z','Y'), 'acct_type':('00','3A'),
                      'cons_acct_num':('0032','0033'), 'credit_limit':(10,20),
                      'hcola':(-1,-1), 'port_type':('I','M'),
                      'terms_dur':('5','10'),  'terms_freq':('P','W')}
        # Create the parent records for the AccountActivity data for second event
        event_2 = Metro2Event(name='test_exam2')
        event_2.save()
        self.file2 = M2DataFile(event=event_2, file_name='file2.txt')
        self.file2.save()
        # Create the Account Holders
        self.account_holders = self.create_bulk_account_holders(self.file2, ('Z','Y'))
        self.account_activity = self.create_bulk_activities(self.file2, activities2, 2)

    ############################
    # Tests for the models
    def test_get_all_account_activity_returns_results(self):
        self.create_exam_activity()
        evl = EvaluatorMetaData(name="Test")
        evl.set_func(func="test")
        evl.set_metro2_event(event='test_exam')
        result = evl.get_all_account_activity()

        self.assertEqual(2, len(result))

    def test_get_all_account_activity_returns__no_results(self):
        self.create_exam_activity()
        evl = EvaluatorMetaData(name="Test")
        evl.set_func(func="test")
        evl.set_metro2_event(event='no_exam')
        result = evl.get_all_account_activity()

        self.assertEqual(0, len(result))

    def test_set_func_sets_func(self):
        evl = EvaluatorMetaData(name="Test")
        evl.set_func(func=self.set_mock_function)

        self.assertEqual(self.set_mock_function, evl.func)

    def set_mock_function(self):
        return 'test'

    def mock_custom_function(self):
        return [{'id':1, 'name':'Test_1'}, {'id':2, 'name':'Test_2'}]
