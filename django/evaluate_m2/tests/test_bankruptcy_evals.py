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
    # 1. ( cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ||
    #      account_holder__cons_info_ind_assoc == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' )
    # 2. acct_stat != '05', '13', '61', '62', '63', '64', '65', 'DA', 'DF'
    # 3. dofd == None
    def test_eval_bkrpcy_dofd_1(self):
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'dofd': None, 'cons_info_ind': 'A',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'dofd': None, 'cons_info_ind': 'J',
                'cons_info_ind_assoc': ['C','J']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'78', 'dofd': date(2019, 12, 31), 'cons_info_ind': 'B',
                'cons_info_ind_assoc': ['K', 'L']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'dofd': None, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': ['M', 'L']
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'82', 'dofd': None, 'cons_info_ind': 'M',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-dofd=01012020,
        # 35: NO-acct-stat=13, 36: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat': '11',
            'account_holder__cons_info_ind': 'A',
            'account_holder__cons_info_ind_assoc': [],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat': '71',
            'account_holder__cons_info_ind': 'J',
            'account_holder__cons_info_ind_assoc': ['C','J'],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-DOFD-1', expected)

    # Hits when all conditions met:
    # 1. ( cons_info_ind == 'R', 'V' || account_holder__cons_info_ind_assoc == 'R', 'V' )
    # 2. acct_stat != '05', '97', 'DA', 'DF'
    # 3. dofd == None
    def test_eval_bkrpcy_dofd_2(self):

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'dofd': None, 'cons_info_ind': 'R',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'dofd': None, 'cons_info_ind': 'J',
                'cons_info_ind_assoc': ['V','J']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'71', 'dofd': date(2019, 12, 31), 'cons_info_ind': 'R',
                'cons_info_ind_assoc': ['K', 'L']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'05', 'dofd': None, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': ['M', 'V']
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'82', 'dofd': None, 'cons_info_ind': 'M',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-dofd=01012020,
        # 35: NO-acct-stat=05, 36: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat': '11',
            'account_holder__cons_info_ind': 'R',
            'account_holder__cons_info_ind_assoc': [],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat': '13',
            'account_holder__cons_info_ind': 'J',
            'account_holder__cons_info_ind_assoc': ['V','J'],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-DOFD-2', expected)

    # Hits when all conditions met:
    # 1. ( cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'R', 'V' ||
    #      account_holder__cons_info_ind_assoc == 'A', 'B', 'C', 'D', 'E', 'F', 'R', 'V' )
    # 2. acct_stat == '97'
    # 3. dofd == None
    def test_eval_bkrpcy_dofd_3(self):

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)

        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97', 'dofd': None, 'cons_info_ind': 'A',
                'cons_info_ind_assoc': []
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97', 'dofd': None, 'cons_info_ind': 'J',
                'cons_info_ind_assoc': ['C','J']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'97', 'dofd': date(2019, 12, 31), 'cons_info_ind': 'B',
                'cons_info_ind_assoc': ['K', 'L']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'dofd': None, 'cons_info_ind': 'E',
                'cons_info_ind_assoc': ['M', 'L']
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'13', 'dofd': None, 'cons_info_ind': 'M',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-dofd=01012020,
        # 35: NO-acct-stat=13, 36: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'acct_stat': '97',
            'account_holder__cons_info_ind': 'A',
            'account_holder__cons_info_ind_assoc': [],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'acct_stat': '97',
            'account_holder__cons_info_ind': 'J',
            'account_holder__cons_info_ind_assoc': ['C','J'],
            'dofd': None, 'amt_past_due': 0, 'current_bal': 0,
            'date_closed': None, 'smpa': 0
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-DOFD-3', expected)

    # Hits when all conditions met:
    # 1. dofd == None
    # 2. (cons_info_ind == 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Z', 'V', '1A' ||
    #     account_holder__cons_info_ind_assoc == 'A', 'B', 'C', 'D', 'E', 'F',
    #                                            'G', 'H', 'Z', 'V', '1A')
    def test_eval_bkrpcy_dofd_4(self):
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
                'dofd': date(2019, 12, 31), 'cons_info_ind': 'B',
                'cons_info_ind_assoc': ['K', 'L']
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'dofd': None, 'cons_info_ind': 'I',
                'cons_info_ind_assoc': []
            }]
        for item in activities:
            acct_record(self.data_file, item)

        # 32: HIT, 33: HIT, 34: NO-dofd=01012020,
        # 35: NO-all cons_info_ind not valid

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'account_holder__cons_info_ind_assoc': [], 'dofd': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'J',
            'account_holder__cons_info_ind_assoc': ['C','J'], 'dofd': None
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-DOFD-4', expected)

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

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'account_holder__cons_info_ind': 'A',
            'account_holder__ecoa_assoc': ['3','3']
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'account_holder__cons_info_ind': 'B',
            'account_holder__ecoa_assoc': ['3']
        }]
        self.assert_evaluator_correct(self.event, 'Bankruptcy-ECOA-1', expected)