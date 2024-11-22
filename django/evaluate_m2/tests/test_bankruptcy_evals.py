from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper, acct_record
from parse_m2.models import Metro2Event, M2DataFile

class BankruptcyEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the category addl bk evaluators

    # Hits when all conditions met:
    # 1. amt_past_due ≤ 0
    # 2. acct_stat != '05', '13', '61', '62', '63', '64', '65', 'DA', 'DF'
    # 3. (cons_info_ind == 'E', 'F', 'G', 'H') ||
    #    (account_holder__cons_info_ind_assoc == 'E', 'F', 'G', 'H')
    def test_eval_bkrpcy_apd_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat': '71', 'amt_past_due': 0, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat': '82', 'amt_past_due': -12, 'cons_info_ind': 'G',
                'cons_info_ind_assoc': []
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat': '80', 'amt_past_due': 0, 'cons_info_ind': '',
                'cons_info_ind_assoc': ['H']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat': '71', 'amt_past_due': 2000, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': []
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat': '13', 'amt_past_due': 0, 'cons_info_ind': 'G',
                'cons_info_ind_assoc': []
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat': '80', 'amt_past_due': 0, 'cons_info_ind': '',
                'cons_info_ind_assoc': []
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat': '80', 'amt_past_due': 0, 'cons_info_ind': '',
                'cons_info_ind_assoc': ['A']
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: HIT,
        # 35: NO-amt_past_due > 0, 36: NO-acct_stat='13',
        # 37: NO-cons_info_ind='' & cons_info_ind_assoc=[], 
        # 38: NO-cons_info_ind='' & cons_info_ind_assoc=['A']

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034',
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-APD-1', expected)

    # Hits when all conditions met:
    # 1. current_bal ≤ 0
    # 2. acct_stat != '05', '13', '61', '62', '63', '64', '65', 'DA', 'DF'
    # 3. (cons_info_ind == 'E', 'F', 'G', 'H') ||
    #    (account_holder__cons_info_ind_assoc == 'E', 'F', 'G', 'H')
    def test_eval_bkrpcy_bal_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat': '71', 'current_bal': 0, 'cons_info_ind': 'F',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat': '82', 'current_bal': -150, 'cons_info_ind': 'H',
                'cons_info_ind_assoc': []
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat': '80', 'current_bal': 0, 'cons_info_ind': '',
                'cons_info_ind_assoc': ['E']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat': '71', 'current_bal': 150, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': []
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat': '61', 'current_bal': 0, 'cons_info_ind': 'G',
                'cons_info_ind_assoc': []
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat': '80', 'current_bal': 0, 'cons_info_ind': '',
                'cons_info_ind_assoc': []
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat': '80', 'current_bal': 0, 'cons_info_ind': 'B',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: HIT,
        # 35: NO-current_bal > 0, 36: NO-acct_stat='61',
        # 37: NO-cons_info_ind='' & cons_info_ind_assoc=[], 
        # 38: NO-cons_info_ind='B' & cons_info_ind_assoc=[]

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034',
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-Balance-1', expected)

    # Hits when all conditions met:
    # 1. dofd == None
    # 2. (cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A', 'R' ||
    #     account_holder__cons_info_ind_assoc == 'A', 'B', 'C', 'D', 'E', 'F',
    #                                            'G', 'H', 'Z', 'V', '1A', 'R')
    def test_eval_bkrpcy_dofd_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'dofd': None, 'cons_info_ind': 'A',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'dofd': None, 'cons_info_ind': 'J',
                'cons_info_ind_assoc': ['C','J']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'dofd': None, 'cons_info_ind': 'R',
                'cons_info_ind_assoc': []
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'dofd': date(2019, 12, 31), 'cons_info_ind': 'B',
                'cons_info_ind_assoc': ['K', 'L']
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'dofd': None, 'cons_info_ind': 'I',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: HIT,
        # 35: NO-dofd=01012020, 36: NO-all cons_info_ind not valid

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034',
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-DOFD-1', expected)

    # Hits when all conditions met:
    # 1. (cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A')
    # 2. ecoa_assoc = '3'
    def test_eval_bkrpcy_ecoa_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'dofd': None, 'cons_info_ind': 'A',
                'ecoa_assoc': ['3','3']
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'dofd': None, 'cons_info_ind': 'B',
                'ecoa_assoc': ['3']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'dofd': date(2019, 12, 31), 'cons_info_ind': 'C',
                'ecoa_assoc': ['5']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'dofd': None, 'cons_info_ind': 'I',
                'ecoa_assoc': ['3']
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-ecoa_assoc='5'
        # 35: NO-cons_info_ind='I'

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-ECOA-1', expected)

 # Hits when all conditions met:
    # 1. smpa > 0
    # 2. acct_stat != '05', '13', '61', '62', '63', '64', '65', 'DA', 'DF'
    # 3. (cons_info_ind == 'E', 'F', 'G', 'H') ||
    #    (account_holder__cons_info_ind_assoc == 'E', 'F', 'G', 'H')
    def test_eval_bkrpcy_smpa_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat': '71', 'smpa': 1000, 'cons_info_ind': 'F',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat': '82', 'smpa': 100, 'cons_info_ind': 'H',
                'cons_info_ind_assoc': []
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat': '80', 'smpa': 225, 'cons_info_ind': '',
                'cons_info_ind_assoc': ['E']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat': '71', 'smpa': 0, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': []
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat': '61', 'smpa': 100, 'cons_info_ind': 'G',
                'cons_info_ind_assoc': []
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat': '80', 'smpa': 140, 'cons_info_ind': '',
                'cons_info_ind_assoc': []
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat': '80', 'smpa': 180, 'cons_info_ind': 'B',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: HIT,
        # 35: NO-smpa = 0, 36: NO-acct_stat='61',
        # 37: NO-cons_info_ind='' & cons_info_ind_assoc=[], 
        # 38: NO-cons_info_ind='B' & cons_info_ind_assoc=[]

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034',
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-SMPA-1', expected)