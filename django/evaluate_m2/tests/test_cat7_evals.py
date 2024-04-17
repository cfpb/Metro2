from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import K2, Metro2Event, M2DataFile


class Cat7_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W'))

    def create_data(self, activities, size):
        self.create_bulk_activities(self.data_file, activities, size)
        # Create the segment data
        self.create_bulk_k2()

    def create_bulk_k2(self):
        # Create the segment data
        self.k2 = K2.objects.bulk_create([
            self.create_k2(32, 'a', 'hit'),
            self.create_k2(34, 'b', 'no1'),
            self.create_k2(35, 'c', 'no2')
        ])

    def create_other_segments(self):
        # Create the other segment data
        self.j1 = self.create_jsegment(32, 'j1', 'a1')
        self.j1.save()
        self.j2 = self.create_jsegment(32, 'j2', 'a2')
        self.j2.save()
        self.l1 = self.create_l1(32)
        self.l1.save()

    ############################
    # Tests for the category 7 evaluators
    def test_eval_7_paid_but_account_status_shows_not_paid(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'AU', 'AX', 'BP', 'C'
        # 2. acct_stat != '13', '61', '62', '63', '64', '65'
        # Create the Account Activities data
        activities = { 'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-acct_stat=65
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'C', 'acct_stat': '71', 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'AX', 'acct_stat': '11', 'amt_past_due': 9, 'current_bal': 9,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event,
            'SCC-Status-1', expected)

    def test_eval_7_paid_but_account_has_balance(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AU', 'AX', 'BP', 'C'
        # 2. current_bal != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(200,-9,100,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-current_bal=0
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'C', 'acct_stat': '71', 'amt_past_due': 0, 'current_bal': 200,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'AX', 'acct_stat': '11', 'amt_past_due': 9, 'current_bal': -9,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'SCC-Balance-1',
            expected)

    def test_eval_7_paid_but_account_has_APD(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AU', 'AX', 'BP', 'C'
        # 2. amt_past_due != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(200,9,20,0), 'current_bal':(0,9,0,0),
            'spc_com_cd':('C','AX','WT','AU')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-amt_past_due=0
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'C', 'acct_stat': '71', 'amt_past_due': 200, 'current_bal': 0,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'AX', 'acct_stat': '11', 'amt_past_due': 9, 'current_bal': 9,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'SCC-APD-1',
            expected)

    def test_eval_7_transferred_purchased_but_account_has_balance(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AH', 'AT', 'O'
        # 2. current_bal != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'amt_past_due':(0,9,0,0), 'current_bal':(200,9,100,0),
            'spc_com_cd':('AT','O','WT','AH')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-current_bal=0
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'AT', 'acct_stat': '71', 'amt_past_due': 0, 'current_bal': 200,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'O', 'acct_stat': '11', 'amt_past_due': 9, 'current_bal': 9,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'SCC-Balance-2', expected)

    def test_eval_7_transferred_purchased_but_account_has_APD(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AH', 'AT', 'O'
        # 2. amt_past_due != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'), 'amt_past_due':(200,-9,10,0), 'current_bal':(0,9,0,100),
            'spc_com_cd':('AT','O','WT','AH')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=WT, 4: NO-amt_past_due=0
        self.create_data(activities, 4)
        self.create_other_segments()

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'account_holder__cons_info_ind': 'Z', 'spc_com_cd': 'AT', 'acct_stat': '71', 'amt_past_due': 200,
            'current_bal': 0, 'date_closed': date(2020, 1, 1), 'j1__cons_info_ind': 'a1',
            'j2__cons_info_ind': 'a2', 'k2__purch_sold_ind': 'a', 'l1__change_ind': '1'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'account_holder__cons_info_ind': 'Y', 'spc_com_cd': 'O', 'acct_stat': '11', 'amt_past_due': -9,
            'current_bal': 9, 'date_closed': date(2020, 1, 1), 'j1__cons_info_ind': None,
            'j2__cons_info_ind': None, 'k2__purch_sold_ind': None, 'l1__change_ind': None
        }]

        self.assert_evaluator_correct(
            self.event, 'SCC-APD-2', expected)

    def test_eval_7_terminated_owing_balance_but_no_current_balance(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BD', 'BG', 'BI', 'BK'
        # 2. current_bal <= 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'acct_type':('08','26','0','0'), 'amt_past_due':(200,9,0,0),
            'current_bal':(-1,0,-1,5), 'spc_com_cd':('BD','BK','AI','BG')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=AI, 4: NO-current_bal=5
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'BD', 'acct_stat': '71', 'acct_type': '08','amt_past_due': 200, 'current_bal': -1,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'BK', 'acct_stat': '11',  'acct_type': '26','amt_past_due': 9, 'current_bal': 0,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'SCC-Balance-4', expected)

    def test_eval_7_terminated_owing_balance_but_no_APD(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BD', 'BG', 'BI', 'BK'
        # 2. amt_past_due <= 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'), 'acct_stat':('71','11','71','65'),
            'acct_type':('08','26','0','0'), 'amt_past_due':(-200,0,-1,1),
            'current_bal':(0,9,10,100), 'spc_com_cd':('BD','BK','AI','BG')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=AI, 4: NO-amt_past_due=1
        self.create_data(activities, 4)
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'BD', 'acct_stat': '71', 'acct_type': '08','amt_past_due': -200, 'current_bal': 0,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'BK', 'acct_stat': '11',  'acct_type': '26','amt_past_due': 0, 'current_bal': 9,
            'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, '7-Terminated owing balance, but no APD', expected)

    def test_eval_7_account_satisfied_but_has_balance(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BC', 'BF', 'BJ'
        # 2. current_bal != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','W','X'), 'acct_stat':('71','11','71','65'),
            'acct_type':('08','26','0','0'), 'amt_past_due':(0,9,0,0),
            'current_bal':(200,-9,10,0), 'spc_com_cd':('BC','BJ','BP','BF')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=BP, 4: NO-current_bal=0
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'BC', 'acct_stat': '71', 'acct_type': '08','amt_past_due': 0,
            'current_bal': 200, 'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'BJ', 'acct_stat': '11',  'acct_type': '26','amt_past_due': 9,
            'current_bal': -9, 'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'SCC-Balance-3', expected)

    def test_eval_7_account_satisfied_but_has_APD(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BC', 'BF', 'BJ'
        # 2. amt_past_due != 0

        # Create the Account Activities data
        activities = {'id':(32,33,34,35), 'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','W','X'), 'acct_stat':('71','11','71','65'),
            'acct_type':('08','26','0A','0G'), 'amt_past_due':(200,-9,10,0),
            'current_bal':(0,9,10,100), 'spc_com_cd':('BC','BJ','BP','BF')}
        # 1: HIT, 2: HIT, 3: NO-spc_com_cd=BP, 4: NO-amt_past_due=0
        self.create_data(activities, 4)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'spc_com_cd': 'BC', 'acct_stat': '71', 'acct_type': '08','amt_past_due': 200,
            'current_bal': 0, 'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': 'a'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'spc_com_cd': 'BJ', 'acct_stat': '11',  'acct_type': '26','amt_past_due': -9,
            'current_bal': 9, 'date_closed': date(2020, 1, 1), 'k2__purch_sold_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, "SCC-APD-3", expected)
