from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class Cat11_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the category 11 evaluators



    def test_eval_11_fcl_with_curr_pmt_rtg_but_amt_past_due(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '89'
    # 2. pmt_rating == '0'
    # 3. amt_past_due > 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89', 'pmt_rating':'0', 'amt_past_due': 5
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'89', 'pmt_rating':'0', 'amt_past_due': 10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'88', 'pmt_rating':'0', 'amt_past_due': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'89', 'pmt_rating':'1', 'amt_past_due': 20
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'89', 'pmt_rating':'0', 'amt_past_due': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=88,
        # 35: NO-pmt_rating=1, 36: NO-amt_past_due=0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '89', 'amt_past_due': 5, 'pmt_rating': '0',
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '',
            'terms_freq': '00', 'acct_type': '', 'port_type': 'A'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '89', 'amt_past_due': 10, 'pmt_rating': '0',
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '',
            'terms_freq': '00', 'acct_type': '', 'port_type': 'A'
        }]

        self.assert_evaluator_correct(self.event, 'Rating-APD-1', expected)

    def test_eval_11_fcl_with_delinquent_pmt_rtg_but_no_amt_past_due(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '89','94'
    # 2. pmt_rating == '1', '2', '3', '4', '5', '6', 'G', 'L'
    # 3. amt_past_due == 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89', 'pmt_rating':'1', 'amt_past_due': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'94', 'pmt_rating':'2', 'amt_past_due': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'88', 'pmt_rating':'3', 'amt_past_due': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'89', 'pmt_rating':'F', 'amt_past_due': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'94', 'pmt_rating':'G', 'amt_past_due': 1
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=88,
        # 35: NO-pmt_rating=F, 36: NO-amt_past_due=0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '89', 'amt_past_due': 0, 'pmt_rating': '1',
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '',
            'terms_freq': '00', 'acct_type': '', 'port_type': 'A'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '94', 'amt_past_due': 0, 'pmt_rating': '2',
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '',
            'terms_freq': '00', 'acct_type': '', 'port_type': 'A'
        }]

        self.assert_evaluator_correct(self.event, 'Rating-APD-2', expected)





