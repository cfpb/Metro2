from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class DeferredEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        self.expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}]

    def test_eval_deferred_balance_1(self):
    # Hits when all conditions are met:
    # 1. port_type == 'O', 'R'
    # 2. acct_type == '18', '37', '2A', '8A'
    # 3. acct_stat == '11'
    # 4. terms_freq == 'D'
    # 5. compl_cond_cd == 'XA'
    # 6. current_bal == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'acct_type':'18', 'port_type':'O',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'acct_type':'37', 'port_type':'R',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'acct_type':'2A', 'port_type':'A',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'11', 'acct_type':'2C',  'port_type':'O',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'81', 'acct_type':'8A', 'port_type':'R',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'11', 'acct_type':'18', 'port_type':'O',
                'compl_cond_cd': 'XA', 'current_bal': 0, 'terms_freq': '0'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'11', 'acct_type':'37', 'port_type':'R',
                'compl_cond_cd': 'XB', 'current_bal': 0, 'terms_freq': 'D'
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'acct_stat':'11', 'acct_type':'2A', 'port_type':'O',
                'compl_cond_cd': 'XA', 'current_bal': 1, 'terms_freq': 'D'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=A, 35: NO-acct_type=2C,
        # 36: NO-acct_stat=81, 37: terms_freq=0, 38: compl_cond_cd=XB,
        # 39: current_bal=1

        self.assert_evaluator_correct(
            self.event, 'Deferred-Balance-1', self.expected)


    def test_eval_deferred_smpa_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '11','71','78','80','82','83','84','93'
    # 2. terms_freq == 'D'
    # 3. smpa > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'terms_freq':'D', 'smpa': 5
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'terms_freq':'D', 'smpa':10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'88', 'terms_freq':'D', 'smpa':15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'78', 'terms_freq':'P', 'smpa':20
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'80', 'terms_freq':'D', 'smpa': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=88,
        # 35: NO-terms_freq=P, 36: NO-smpa=0,

        self.assert_evaluator_correct(
            self.event, 'Deferred-SMPA-1', self.expected)
