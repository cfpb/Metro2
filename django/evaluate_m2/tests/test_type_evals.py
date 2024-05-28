from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper, acct_record
from parse_m2.models import Metro2Event, M2DataFile


class TypeEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V','U','T'))

    ############################
    # Tests for the category 12 evaluators
    def test_type_balance_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_stat == '11'
        # 3. acct_type == '00', '01', '02', '03', '04', '05', '06', '10', '11',
        #                 '13', '17', '20', '29', '65', '66', '67', '68', '69',
        #                 '70', '71', '72', '73', '74', '75', '91', '95', '0A',
        #                 '0F', '3A', '6A', '6D', '7B', '9A'
        # 4. spc_com_cd == 'BS'
        # 5. current_bal > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'00',
                'spc_com_cd': 'BS', 'current_bal': 25
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'01',
                'spc_com_cd': 'BS', 'current_bal': 20
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_stat':'11', 'acct_type':'02',
                'spc_com_cd': 'BS', 'current_bal': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_stat':'05', 'acct_type':'03',
                'spc_com_cd': 'BS', 'current_bal': 10
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'07',
                'spc_com_cd': 'BS', 'current_bal': 5
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'04',
                'spc_com_cd': 'AU', 'current_bal': 1
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'05',
                'spc_com_cd': 'BS', 'current_bal': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: NO-port_type=C, 34: NO-acct_stat=5, 35: NO-acct_type=07,
        # 36: NO-spc_com_cd=AU, 37: NO-current_bal=0

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032', 'acct_type': '00', 'acct_stat': '11', 'port_type': 'I', 'current_bal': 25,
            'spc_com_cd': 'BS', 'amt_past_due': 0, 'compl_cond_cd': '',
            'date_closed': None,  'dofd': None,'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033', 'acct_type': '01', 'acct_stat': '11', 'port_type': 'I', 'current_bal': 20,
            'spc_com_cd': 'BS', 'amt_past_due': 0, 'compl_cond_cd': '',
            'date_closed': None,  'dofd': None,'orig_chg_off_amt': 0, 'smpa':0,
            'terms_freq':"00"
        }]
        self.assert_evaluator_correct(self.event, "Type-Balance-1", expected)

    def test_eval_type_hcola_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '00', '3A', '10', '91', '6A', '7B', '05',
        #                 '0A', '0F', '47', '9A', '17', '01', '02',
        #                 '03', '11', '13', '04', '20', '6D', '06'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'00', 'hcola': -1, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'M', 'acct_type':'3A', 'hcola': -1, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'12', 'hcola': -5, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'91', 'hcola': -5, 'terms_freq': 'D'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'00', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'3A', 'hcola': 5, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: NO-port_type=M, 34: NO-acct_type=12, 35: NO-terms_freq=D,
        # 36: HIT, 37: NO-hcola=5

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032', 'acct_type': '00', 'port_type': 'I', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 0, 'terms_dur': '00'
        }, {
            'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036', 'acct_type': '00', 'port_type': 'I', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 0, 'terms_dur': '00'
        }]
        self.assert_evaluator_correct(self.event, 'Type-HCOLA-1', expected)

    def test_eval_type_hcola_2(self):
        # Hits when all conditions are met:
        # 1. port_type == 'M'
        # 2. acct_type == '08', '19', '25', '26', '2C', '5A', '5B', '6B'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'M', 'acct_type':'08', 'hcola': -1, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_type':'19', 'hcola': -1, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'M', 'acct_type':'11', 'hcola': -5, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'M', 'acct_type':'25', 'hcola': -5, 'terms_freq': 'D'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'M', 'acct_type':'2C', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'M', 'acct_type':'26', 'hcola': 5, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: NO-port_type=I, 34: NO-acct_type=11, 35: NO-terms_freq=D,
        # 36: HIT, 37: NO-hcola=5

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032', 'acct_type': '08', 'port_type': 'M', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 0, 'terms_dur': '00'
        }, {
            'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036', 'acct_type': '2C', 'port_type': 'M', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 0, 'terms_dur': '00'
        }]
        self.assert_evaluator_correct(self.event, 'Type-HCOLA-2', expected)

    def test_eval_type_hcola_3(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '0C', '48', '77'
        # 3. terms_freq != 'D'
        # 4. hcola <= 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'O', 'acct_type':'0C', 'hcola': -1, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_type':'48', 'hcola': -1, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'O', 'acct_type':'11', 'hcola': -5, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'77', 'hcola': -5, 'terms_freq': 'D'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'0C', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'48', 'hcola': 5, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: NO-port_type=I, 34: NO-acct_type=11, 35: NO-terms_freq=D,
        # 36: HIT, 37: NO-hcola=5
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032', 'acct_type': '0C', 'port_type': 'O', 'hcola': -1,
            'terms_freq': 'P', 'credit_limit': 0, 'terms_dur': '00'
        }, {
            'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036', 'acct_type': '0C', 'port_type': 'O', 'hcola': 0,
            'terms_freq': 'W', 'credit_limit': 0, 'terms_dur': '00'
        }]
        self.assert_evaluator_correct(self.event, "Type-HCOLA-3", expected)
