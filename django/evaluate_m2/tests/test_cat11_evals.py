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
    def test_eval_11_not_charged_off_but_original_charge_off_amount(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05', '11', '13', '62', '65', '71', '78',
    #                 '80', '82', '83', '84', '89', '93'
    # 2. orig_chg_off_amt > 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'orig_chg_off_amt': 5
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11',  'orig_chg_off_amt': 1
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12',  'orig_chg_off_amt': 1
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'orig_chg_off_amt': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12,
        # 35: NO-orig_chg_off_amt=0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'05', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'orig_chg_off_amt': 5, 'smpa':0,
            'spc_com_cd':"", 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'11', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'orig_chg_off_amt': 1, 'smpa':0,
            'spc_com_cd':"", 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-ChargeOff-1', expected)

    def test_eval_11_transferred_delinquent_pmt_rtg_no_dofd(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '5'
    # 2. pmt_rating == '1', '2', '3', '4', '5', '6', 'G', 'L'
    # 3. dofd == None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'pmt_rating':'1', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'pmt_rating':'G', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'pmt_rating':'1', 'acct_stat':'01', 'dofd':None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'pmt_rating':'7', 'acct_stat':'05', 'dofd':date(2019, 12, 31)
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'pmt_rating':'7', 'acct_stat':'01', 'dofd':None
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=01,
        # 35: NO-dofd=date(2019, 12, 31), 36: NO-pmt_rating=7

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'05', 'dofd': None,
            'pmt_rating':'1', 'amt_past_due': 0, 'compl_cond_cd':"",
            'current_bal':0, 'date_closed': None, 'orig_chg_off_amt': 0,
            'smpa':0, 'spc_com_cd':"", 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'05', 'dofd': None,
            'pmt_rating':'G', 'amt_past_due': 0, 'compl_cond_cd':"",
            'current_bal':0, 'date_closed': None, 'orig_chg_off_amt': 0,
            'smpa':0, 'spc_com_cd':"", 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-DOFD-3', expected)

    def test_eval_status_balance_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05','13','61','62','63','64','65'
    # 2. current_bal > 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'current_bal':5,
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'current_bal':10,
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'01', 'current_bal':15,
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'61', 'current_bal':0,
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=01, 35: NO-current_bal=0,

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'05', 'current_bal': 5,
            'amt_past_due': 0, 'compl_cond_cd':"", 'dofd': None,
            'date_closed': None, 'orig_chg_off_amt': 0,
            'smpa':0, 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'13', 'current_bal': 10,
            'amt_past_due': 0, 'compl_cond_cd':"", 'dofd': None,
            'date_closed': None, 'orig_chg_off_amt': 0,
            'smpa':0, 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-Balance-1', expected)

    def test_eval_status_smpa_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05','13','62','64','65','97'
    # 2. smpa > 0
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'smpa':5
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'smpa':10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'01', 'smpa':15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'smpa':0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=01, 35: NO-smpa=0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'05', 'smpa':5,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'13', 'smpa': 10,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-SMPA-1', expected)

    def test_eval_11_charged_off_but_no_charge_off_amount(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '64', '97'
    # 2. orig_chg_off_amt == 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'64', 'orig_chg_off_amt': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97',  'orig_chg_off_amt': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12',  'orig_chg_off_amt': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'64', 'orig_chg_off_amt': 5
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12,
        # 35: NO-orig_chg_off_amt=5

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'64', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'spc_com_cd':"", 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'97', 'dofd': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
            'date_closed': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'spc_com_cd':"", 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-ChargeOff-2', expected)

    def test_eval_ccc_date_closed_3(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '97'
    # 2. compl_cond_cd != 'XA'
    # 3. date_closed != None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97', 'compl_cond_cd': 'XB', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97',  'compl_cond_cd': 'XC', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12',  'compl_cond_cd': 'XD', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'97', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'97', 'compl_cond_cd': 'XE', 'date_closed': None
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12,
        # 35: NO-compl_cond_cd=XA, 36: No-date_closed=None

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'97', 'compl_cond_cd':"XB",
            'date_closed': date(2020, 1, 1),'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'97', 'compl_cond_cd':"XC",
            'date_closed': date(2020, 1, 1),'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(self.event, 'CCC-DateClosed-3', expected)

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

        self.assert_evaluator_correct(
            self.event,
            'Rating-APD-1',
            expected)

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

        self.assert_evaluator_correct(
            self.event,
            'Rating-APD-2',
            expected)

    def test_eval_11_current_but_dofd(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '11'
    # 2. dofd != None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'dofd':date(2019, 12, 31)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'dofd':date(2019, 12, 31)
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'1', 'dofd':date(2019, 12, 31)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'1', 'dofd':None
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-acct_stat=01, 35: NO-dofd=None

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032', 'acct_stat':'11', 'dofd': date(2019, 12, 31), 'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0, 'date_closed': None,
            'orig_chg_off_amt': 0, 'smpa':0, 'spc_com_cd':"", 'terms_freq':"00",
            'account_holder__cons_info_ind': '', 'j1__cons_info_ind': None, 'j2__cons_info_ind': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat':'11', 'dofd': date(2019, 12, 31), 'amt_past_due': 0,
            'compl_cond_cd':"", 'current_bal':0, 'date_closed': None,
            'orig_chg_off_amt': 0, 'smpa':0, 'spc_com_cd':"", 'terms_freq':"00",
            'account_holder__cons_info_ind': '', 'j1__cons_info_ind': None, 'j2__cons_info_ind': None
        }]
        self.assert_evaluator_correct(
            self.event, 'Status-DOFD-6', expected)

    def test_eval_11_current_delinquent_not_closed_but_date_closed(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '11','71','78','80','82','83','84','93'
    # 2. compl_cond_cd != 'XA'
    # 3. date_closed != None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'compl_cond_cd': 'XB', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71',  'compl_cond_cd': 'XC', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12',  'compl_cond_cd': 'XD', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'78', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'80', 'compl_cond_cd': 'XE', 'date_closed': None
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12,
        # 35: NO-compl_cond_cd=XA, 36: No-date_closed=None

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'11', 'compl_cond_cd':"XB",
            'date_closed': date(2020, 1, 1),'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'71', 'compl_cond_cd':"XC",
            'date_closed': date(2020, 1, 1),'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(self.event, 'Status-DateClosed-2', expected)

    def test_eval_ccc_date_closed_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '11','71','78','80','82','83','84','93'
    # 2. compl_cond_cd == 'XA'
    # 3. date_closed == None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'78', 'compl_cond_cd': 'XB', 'date_closed': None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'80', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12,
        # 35: NO-compl_cond_cd=XB, 36: No-date_closed=date(2020, 1, 1)

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'11', 'compl_cond_cd':"XA",
            'date_closed': None,'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'71', 'compl_cond_cd':"XA",
            'date_closed': None,'amt_past_due': 0, 'current_bal':0,
            'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0, 'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'CCC-DateClosed-1', expected)

    def test_eval_11_repossession_but_no_amt_past_due(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '95','96'
    # 2. acct_type == '00', '13', '3A'
    # 3. port_type == 'I'
    # 4. amt_past_due == 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'95', 'acct_type':'00', 'port_type':'I', 'amt_past_due': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'96', 'acct_type':'13', 'port_type':'I', 'amt_past_due': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'88', 'acct_type':'3A', 'port_type':'I', 'amt_past_due': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'96', 'acct_type':'88', 'port_type':'I', 'amt_past_due': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'95', 'acct_type':'00', 'port_type':'1', 'amt_past_due': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'96', 'acct_type':'13', 'port_type':'I', 'amt_past_due': 25
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=3,
        # 35: NO-acct_type=3, 36: NO-port_type=1,
        # 37: NO-amt_past_due > 0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '95', 'amt_past_due': 0, 'pmt_rating': '', 'compl_cond_cd': '',
            'current_bal': 0, 'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00', 'acct_type': '00',
            'port_type': 'I'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '96', 'amt_past_due': 0, 'pmt_rating': '', 'compl_cond_cd': '',
            'current_bal': 0, 'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00', 'acct_type': '13','port_type': 'I'
        }]

        self.assert_evaluator_correct(
            self.event, '11-repossession but no amount past due', expected)

    def test_eval_ccc_date_closed_2(self):
    # Hits when all conditions are met:
    # 1. port_type == 'C','O','R'
    # 2. acct_stat == '97'
    # 3. compl_cond_cd == 'XA'
    # 4. date_closed == None
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97', 'compl_cond_cd': 'XA', 'date_closed': None,
                'port_type':'C'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97',  'compl_cond_cd': 'XA', 'date_closed': None,
                'port_type':'O'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'97',  'compl_cond_cd': 'XA', 'date_closed': None,
                'port_type':'A'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'78', 'compl_cond_cd': 'XA', 'date_closed': None,
                'port_type':'C'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'97', 'compl_cond_cd': 'XB', 'date_closed': None,'port_type':'O'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'97', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1),
                'port_type':'R'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=A, 35: NO-acct_stat=78,
        # 36: NO-compl_cond_cd=XA, 36: No-date_closed=date(2020, 1, 1)

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'97', 'compl_cond_cd':"XA",
            'date_closed': None, 'port_type':'C', 'amt_past_due': 0,
            'current_bal':0, 'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'97', 'compl_cond_cd':"XA",
            'date_closed': None, 'port_type':'O', 'amt_past_due': 0,
            'current_bal':0, 'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }]
        self.assert_evaluator_correct(
            self.event, 'CCC-DateClosed-2', expected)

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

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '11', 'smpa': 5, 'terms_freq': 'D',  'amt_past_due': 0,
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None, 'dofd': None,
            'orig_chg_off_amt': 0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '71', 'smpa': 10, 'terms_freq': 'D', 'amt_past_due': 0,
            'compl_cond_cd': '', 'current_bal': 0, 'date_closed': None, 'dofd': None,
            'orig_chg_off_amt': 0
        }]

        self.assert_evaluator_correct(
            self.event, 'Deferred-SMPA-1', expected)

    def test_eval_status_apd_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '71','78','80','82','83','84','93','97'
    # 2. compl_cond_cd != 'XA'
    # 3. amt_past_due == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'compl_cond_cd':'XB', 'amt_past_due': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'78', 'compl_cond_cd':'XC', 'amt_past_due': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'79', 'compl_cond_cd':'XD', 'amt_past_due': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80', 'compl_cond_cd':'XA', 'amt_past_due': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'82', 'compl_cond_cd':'XB', 'amt_past_due': 1
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=79,
        # 35: NO-compl_cond_cd=XA, 36: NO-amt_past_due > 0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '71', 'compl_cond_cd': 'XB', 'amt_past_due': 0,
            'pmt_rating': '', 'current_bal': 0, 'date_closed': None, 'dofd': None,
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '78', 'compl_cond_cd': 'XC', 'amt_past_due': 0,
            'pmt_rating': '', 'current_bal': 0, 'date_closed': None, 'dofd': None,
            'orig_chg_off_amt': 0, 'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00'
        }]

        self.assert_evaluator_correct(
            self.event, 'Status-APD-1', expected)

    def test_eval_status_adp_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05','11','13','61','62','63','64','65'
    # 2. amt_past_due > 0
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'amt_past_due': 1
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'amt_past_due': 5
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12', 'amt_past_due': 10
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'amt_past_due': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=12, 35: NO-amt_past_due == 0

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
            'acct_stat': '05', 'amt_past_due': 1, 'pmt_rating': '', 'compl_cond_cd': '',
            'current_bal': 0, 'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00'
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
            'acct_stat': '11', 'amt_past_due': 5, 'pmt_rating': '', 'compl_cond_cd': '',
            'current_bal': 0, 'date_closed': None, 'dofd': None, 'orig_chg_off_amt': 0,
            'smpa': 0, 'spc_com_cd': '', 'terms_freq': '00'
        }]

        self.assert_evaluator_correct(
            self.event, 'Status-APD-2', expected)

    def test_eval_status_date_closed_1_func(self):
        # Hits when all conditions are met:
        # 1. acct_stat == '05', '13', '62', '64', '65', '89', '94'
        # 3. date_closed == None
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'date_closed':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'01', 'date_closed':None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'date_closed':date(2019, 12, 31)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=01, 35: NO-date_closed!=None

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat':'05', 'date_closed': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
             'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat':'13', 'date_closed': None,
            'amt_past_due': 0, 'compl_cond_cd':"", 'current_bal':0,
             'dofd': None, 'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }]
        self.assert_evaluator_correct( self.event,
            'Status-DateClosed-1', expected)
