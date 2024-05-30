from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper, acct_record, l1_record
from parse_m2.models import Metro2Event, M2DataFile

class BalanceEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the balance evaluators
    def test_eval_balance_apd_1(self):
        # hits when both conditions met:
        # 1. port_type == 'I'
        # 2. acct_type == '3A', '13'
        # 3. current_bal == 0
        # 4. l1__change_ind == None
        # 5. amt_past_due > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'I', 'acct_type':'3A', 'current_bal': 0,
                'amt_past_due': 1
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'I','acct_type':'13', 'current_bal': 0,
                'amt_past_due': 5
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'O', 'acct_type':'3A', 'current_bal': 0,
                'amt_past_due': 10
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'I', 'acct_type':'00', 'current_bal': 0,
                'amt_past_due': 15
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'I', 'acct_type':'00', 'current_bal': 1,
                'amt_past_due': 20
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'I', 'acct_type':'00', 'current_bal': 0,
                'amt_past_due': 25
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type': 'I', 'acct_type':'00', 'current_bal': 0,
                'amt_past_due': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_segment = {'id': 37, 'change_ind': '1'}
        l1_record(l1_segment)
        # 32: HIT, 33: HIT, 34: NO-port_type=O,
        # 35: NO-L1.acct_type=00, 36: NO-current_bal=1,
        # 37: NO-l1__change_ind=1, 38: NO-amt_past_due=0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_type':'3A', 'amt_past_due': 1, 'current_bal': 0, 'port_type': 'I',
            'l1__change_ind': None,'acct_stat': '', 'date_closed': None, 'spc_com_cd': ''
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_type':'13', 'amt_past_due': 5, 'current_bal': 0, 'port_type': 'I',
            'l1__change_ind': None,'acct_stat': '', 'date_closed': None, 'spc_com_cd': ''
        }]
        self.assert_evaluator_correct(self.event, 'Balance-APD-1', expected)

    def test_eval_balance_apd_2(self):
        # Hits when both conditions met:
        # 1. current_bal < amt_past_due

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'current_bal':0, 'amt_past_due': 5
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'current_bal':5, 'amt_past_due': 10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'current_bal':10, 'amt_past_due': 10
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'current_bal':11, 'amt_past_due': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-current_bal == amt_past_due
        # 35: NO-current_bal < amt_past_due

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
             'amt_past_due': 5, 'current_bal':0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'amt_past_due': 10, 'current_bal':5
        }]
        self.assert_evaluator_correct(
            self.event, "Balance-APD-2", expected)

    def test_type_date_closed_3(self):
        # Hits when all conditions are met:
        # 1. port_type == 'C', 'M'
        # 2. current_bal > 0
        # 3. spc_com_cd != 'AH', 'AT', 'O'
        # 4. l1_change_ind == None
        # 5. date_closed != None

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'current_bal': 1, 'spc_com_cd': 'AX',
                'date_closed': acct_date
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'M', 'current_bal': 5, 'spc_com_cd': 'AU',
                'date_closed': acct_date
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'R', 'current_bal': 10, 'spc_com_cd': 'BC',
                'date_closed': acct_date
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'current_bal': 0, 'spc_com_cd': 'BD',
                'date_closed': acct_date
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'M', 'current_bal': 15, 'spc_com_cd': 'AH',
                'date_closed': acct_date
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'C', 'current_bal': 20, 'spc_com_cd': 'BF',
                'date_closed': acct_date
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'M', 'current_bal': 25, 'spc_com_cd': 'BG',
                'date_closed': None
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activity = {'id': 37, 'change_ind': '1'}
        l1_record(l1_activity)
        # 32: HIT, 33: HIT, 34: NO-port_type=R, 35: NO-current_bal=0,
        # 36: NO-spc_com_cd=BS, 37: NO-l1_change_ind=1,
        # 38: NO-date_closed=None

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'current_bal': 1, 'date_closed': date(2019, 12, 31), 'l1__change_ind': None,
            'port_type': 'C', 'spc_com_cd': 'AX', 'acct_stat': '', 'amt_past_due': 0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'current_bal': 5, 'date_closed': date(2019, 12, 31), 'l1__change_ind': None,
            'port_type': 'M', 'spc_com_cd': 'AU', 'acct_stat': '', 'amt_past_due': 0
        }]
        self.assert_evaluator_correct(self.event, "Balance-DateClosed-1", expected)