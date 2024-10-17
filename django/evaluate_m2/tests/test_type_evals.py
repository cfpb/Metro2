from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
    l1_record,
)
from parse_m2.models import Metro2Event, M2DataFile


class TypeEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

        # Create the segment data
        self.expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}
        ]
    ############################
    # Tests for the category 12 evaluators
    def test_eval_type_apd_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I', 'M'
        # 2. acct_type != '13', '3A'
        # 3. current_bal == 0
        # 4. spc_com_cd != 'AH', 'AT', 'O'
        # 5. l1_change_ind == None
        # 6. amt_past_due != 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'00', 'current_bal': 0,
                'spc_com_cd': 'BS', 'amt_past_due': 1
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'01', 'current_bal': 0,
                'spc_com_cd': 'BS', 'amt_past_due': 5
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'M', 'acct_type':'13', 'current_bal': 0,
                'spc_com_cd': 'BS', 'amt_past_due': 10
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'02','current_bal': 1,
                'spc_com_cd': 'BS', 'amt_past_due': 150
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'M', 'acct_type':'03', 'current_bal': 0,
                'spc_com_cd': 'AH', 'amt_past_due': 20
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'04', 'current_bal': 0,
                'spc_com_cd': 'AU', 'amt_past_due': 25
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'M', 'acct_type':'05', 'current_bal': 0,
                'spc_com_cd': 'BS', 'amt_past_due': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activity = {'id': 37, 'change_ind': '1'}
        l1_record(l1_activity)
        # 32: HIT, 33: NO-port_type=C, 34: NO-acct_type=13, 35: NO-current_bal=1,
        # 36: NO-spc_com_cd=AH, 37: NO-l1_change_ind=1,
        # 38: NO-amt_past_due=0

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, "Type-APD-1", expected)

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
        # 32: HIT, 33: HIT, 34: NO-port_type=C, 35: NO-acct_stat=5,
        # 36: NO-acct_type=07, 37: NO-spc_com_cd=AU, 38: NO-current_bal=0

        self.assert_evaluator_correct(self.event, 'Type-Balance-1', self.expected)

    def test_eval_type_credit_limit_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '0A', '6A', '9A', '7B', '6D', '0F', '01', '02', '03', '04',
        #                 '05', '06', '10', '11', '13', '17', '20', '47', '91'
        # 3. terms_freq != 'D'
        # 4. credit_limit > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 25
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_type':'6A', 'terms_freq':'P',
                'credit_limit': 20
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'9A', 'terms_freq':'O',
                'credit_limit': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'9B', 'terms_freq':'M',
                'credit_limit': 10
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'6D', 'terms_freq':'D',
                'credit_limit': 5
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'0F', 'terms_freq':'P',
                'credit_limit': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=9B,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=0

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-1', self.expected)

    def test_eval_type_credit_limit_2(self):
        # Hits when all conditions are met:
        # 1. port_type == 'M'
        # 2. acct_type == '08', '19', '25', '26', '2C', '5A', '5B', '6B'
        # 3. terms_freq != 'D'
        # 4. credit_limit > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'M', 'acct_type':'08', 'terms_freq':'M',
                'credit_limit': 25
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'M', 'acct_type':'19', 'terms_freq':'P',
                'credit_limit': 20
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'25', 'terms_freq':'O',
                'credit_limit': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'M', 'acct_type':'27', 'terms_freq':'M',
                'credit_limit': 10
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'M', 'acct_type':'2C', 'terms_freq':'D',
                'credit_limit': 5
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'M', 'acct_type':'5A', 'terms_freq':'P',
                'credit_limit': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=27,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=0

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-2', self.expected)

    def test_eval_type_credit_limit_3(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '0C', '48', '77'
        # 3. terms_freq != 'D'
        # 4. credit_limit > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'O', 'acct_type':'0C', 'terms_freq':'M',
                'credit_limit': 25
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'O', 'acct_type':'48', 'terms_freq':'P',
                'credit_limit': 20
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'77', 'terms_freq':'O',
                'credit_limit': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 10
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'0C', 'terms_freq':'D',
                'credit_limit': 5
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'48', 'terms_freq':'P',
                'credit_limit': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=0

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-3', self.expected)

    def test_eval_type_credit_limit_4(self):
        # Hits when all conditions are met:
        # 1. port_type == 'C'
        # 2. acct_type == '7A', '9B', '15', '43', '47', '89'
        # 3. terms_freq != 'D'
        # 4. credit_limit == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'9B', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'O', 'acct_type':'15', 'terms_freq':'O',
                'credit_limit': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'C', 'acct_type':'43', 'terms_freq':'D',
                'credit_limit': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'C', 'acct_type':'47', 'terms_freq':'P',
                'credit_limit': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=O, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=10

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-4', self.expected)

    def test_eval_type_credit_limit_5(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '2A', '8A', '18', '37', '43'
        # 3. terms_freq != 'D'
        # 4. credit_limit == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'O', 'acct_type':'2A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'O', 'acct_type':'8A', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'18', 'terms_freq':'O',
                'credit_limit': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'37', 'terms_freq':'D',
                'credit_limit': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'43', 'terms_freq':'P',
                'credit_limit': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=10

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-5', self.expected)

    def test_eval_type_credit_limit_6(self):
        # Hits when all conditions are met:
        # 1. port_type == 'R'
        # 2. acct_type == '2A', '8A', '0G', '07', '18', '37', '43'
        # 3. terms_freq != 'D'
        # 4. credit_limit == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'R', 'acct_type':'2A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'R', 'acct_type':'8A', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'0G', 'terms_freq':'O',
                'credit_limit': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'R', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'R', 'acct_type':'37', 'terms_freq':'D',
                'credit_limit': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'R', 'acct_type':'43', 'terms_freq':'P',
                'credit_limit': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-credit_limit=10

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-6', self.expected)

    def test_eval_type_credit_limit_7(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '18'
        # 3. terms_freq != 'D'
        # 4. credit_limit == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'R', 'acct_type':'18', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'0A', 'terms_freq':'O',
                'credit_limit': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'D',
                'credit_limit': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'M',
                'credit_limit': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33:NO-port_type=C, 34: NO-acct_type=0A,
        # 35: NO-terms_freq=D, 36: NO-credit_limit=10

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-7', expected)

    def test_type_date_closed_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type != '13', '3A'
        # 3. current_bal == 0
        # 4. spc_com_cd != 'AH', 'AT', 'O'
        # 5. l1_change_ind == None
        # 6. date_closed == None
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'00', 'current_bal': 0,
                'spc_com_cd': 'BS', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'01', 'current_bal': 0,
                'spc_com_cd': 'BS', 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'13', 'current_bal': 0,
                'spc_com_cd': 'BS', 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'02','current_bal': 1,
                'spc_com_cd': 'BS', 'date_closed': None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'03', 'current_bal': 0,
                'spc_com_cd': 'AH', 'date_closed': None
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'04', 'current_bal': 0,
                'spc_com_cd': 'AU', 'date_closed': None
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'05', 'current_bal': 0,
                'spc_com_cd': 'BS', 'date_closed': acct_date
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activity = {'id': 37, 'change_ind': '1'}
        l1_record(l1_activity)
        # 32: HIT, 33: NO-port_type=C, 34: NO-acct_type=13, 35: NO-current_bal=1,
        # 36: NO-spc_com_cd=AH, 37: NO-l1_change_ind=1,
        # 38: NO-date_closed=date(2019, 12, 31)

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, "Type-DateClosed-1", expected)

    def test_type_date_closed_2(self):
        # Hits when all conditions are met:
        # 1. port_type == 'M'
        # 2. current_bal == 0
        # 3. l1_change_ind == None
        # 4. date_closed == None
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'M', 'current_bal': 0, 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'current_bal': 0, 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'M', 'current_bal': 1, 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'M', 'current_bal': 0, 'date_closed': None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'current_bal': 0, 'date_closed': acct_date
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activity = {'id': 35, 'change_ind': '1'}
        l1_record(l1_activity)
        # 32: HIT, 33: NO-port_type=I, 34: NO-current_bal=1,
        # 35: NO-l1_change_ind=1, 36: NO-date_closed=date(2019, 12, 31)

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, "Type-DateClosed-2", expected)

    def test_type_date_closed_3(self):
        # Hits when all conditions are met:
        # 1. port_type == 'C', 'O', 'R'
        # 2. current_bal == 0
        # 3. spc_com_cd == 'AH', 'AT', 'O'
        # 4. l1_change_ind == None
        # 5. date_closed == None
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'current_bal': 0, 'spc_com_cd': 'AH', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'O', 'current_bal': 0, 'spc_com_cd': 'AT', 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'M', 'current_bal': 0, 'spc_com_cd': 'O', 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'R', 'current_bal': 1, 'spc_com_cd': 'AH', 'date_closed': None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'current_bal': 0, 'spc_com_cd': 'BS', 'date_closed': None
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'current_bal': 0, 'spc_com_cd': 'AT', 'date_closed': None
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'C', 'current_bal': 0, 'spc_com_cd': 'O',
                'date_closed': acct_date
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activity = {'id': 37, 'change_ind': '1'}
        l1_record(l1_activity)
        # 32: HIT, 33: HIT, 34: NO-port_type=I, 35: NO-current_bal=1,
        # 36: NO-spc_com_cd=BS, 37: NO-l1_change_ind=1,
        # 38: NO-date_closed=date(2019, 12, 31)

        self.assert_evaluator_correct(self.event, "Type-DateClosed-3", self.expected)

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

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'}
        ]

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

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'}
        ]

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

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'}
        ]

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-3', expected)

    def test_eval_type_hcola_4(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '2A', '8A', '18', '37'
        # 3. terms_freq != 'D'
        # 4. hcola == 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'O', 'acct_type':'2A', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'O', 'acct_type':'8A', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'18', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'77', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'37', 'hcola': 0, 'terms_freq': 'D'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'2A', 'hcola': 10, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=I, 35: NO-acct_type=77,
        # 36: terms_freq=D, 37: NO-hcola=10

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-4', self.expected)

    def test_eval_type_hcola_5(self):
        # Hits when all conditions are met:
        # 1. port_type == 'R'
        # 2. acct_type == '2A', '8A', '0G', '07', '18', '37'
        # 3. terms_freq != 'D'
        # 4. hcola == 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'R', 'acct_type':'2A', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'R', 'acct_type':'8A', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'0G', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'R', 'acct_type':'77', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'R', 'acct_type':'18', 'hcola': 0, 'terms_freq': 'D'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'R', 'acct_type':'37', 'hcola': 10, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=I, 35: NO-acct_type=77,
        # 36: terms_freq=D, 37: NO-hcola=10

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-5', self.expected)

    def test_eval_type_hcola_6(self):
        # Hits when all conditions are met:
        # 1. port_type == 'C'
        # 2. acct_type == '7A', '9B', '15', '43', '47', '89'
        # 3. terms_freq != 'D'
        # 4. hcola == 0
        # hcola cannot be an empty string or NULL by constraints

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'acct_type':'7A', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'9B', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'I', 'acct_type':'15', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'acct_type':'77', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'C', 'acct_type':'43', 'hcola': 0, 'terms_freq': 'D'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'C', 'acct_type':'47', 'hcola': 10, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=I, 35: NO-acct_type=77,
        # 36: terms_freq=D, 37: NO-hcola=10

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-6', self.expected)

    def test_type_smpa_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_stat == '11'
        # 3. acct_type == '00', '01', '02', '03', '04', '05', '06', '10', '11',
        #                 '13', '17', '20', '29', '65', '66', '67', '68', '69',
        #                 '70', '71', '72', '73', '74', '75', '91', '95', '0A',
        #                 '0F', '3A', '6A', '6D', '7B', '9A'
        # 4. spc_com_cd == 'BS'
        # 5. smpa > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'00',
                'spc_com_cd': 'BS', 'smpa': 25
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'01',
                'spc_com_cd': 'BS', 'smpa': 20
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_stat':'11', 'acct_type':'02',
                'spc_com_cd': 'BS', 'smpa': 15
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_stat':'05', 'acct_type':'03',
                'spc_com_cd': 'BS', 'smpa': 10
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'07',
                'spc_com_cd': 'BS', 'smpa': 5
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'04',
                'spc_com_cd': 'AU', 'smpa': 1
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_stat':'11', 'acct_type':'05',
                'spc_com_cd': 'BS', 'smpa': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=C, 35: NO-acct_stat=5,
        # 36: NO-acct_type=07, 37: NO-spc_com_cd=AU, 38: NO-smpa=0

        self.assert_evaluator_correct(self.event, 'Type-SMPA-1', self.expected)

    def test_eval_type_terms_dur_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'C'
        # 2. acct_type == '7A', '9B', '15', '43', '47', '89'
        # 3. terms_freq != 'D'
        # 4. terms_dur != 'LOC'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': '001'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'9B', 'terms_freq':'P',
                'terms_dur': 'REV'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'O', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': '001'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'acct_type':'0A', 'terms_freq':'M',
                'terms_dur': 'REV'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'C', 'acct_type':'47', 'terms_freq':'D',
                'terms_dur': '001'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'C', 'acct_type':'43', 'terms_freq':'P',
                'terms_dur': 'LOC'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=O, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-terms_dur=LOC

        self.assert_evaluator_correct(self.event, 'Type-TermsDuration-1', self.expected)

    def test_eval_type_terms_dur_2(self):
        # Hits when all conditions are met:
        # 1. port_type == 'O'
        # 2. acct_type == '2A', '8A', '8B', '18', '37'
        # 3. terms_freq != 'D'
        # 4. terms_dur != '001'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'O', 'acct_type':'2A', 'terms_freq':'M',
                'terms_dur': 'LOC'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'O', 'acct_type':'8A', 'terms_freq':'P',
                'terms_dur': 'REV'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'8B', 'terms_freq':'O',
                'terms_dur': 'LOC'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'0A', 'terms_freq':'M',
                'terms_dur': 'REV'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'C', 'acct_type':'18', 'terms_freq':'D',
                'terms_dur': 'LOC'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'C', 'acct_type':'37', 'terms_freq':'P',
                'terms_dur': '001'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-terms_dur=001

        self.assert_evaluator_correct(self.event, 'Type-TermsDuration-2', self.expected)

    def test_eval_type_terms_dur_3(self):
        # Hits when all conditions are met:
        # 1. port_type == 'R'
        # 2. acct_type == '2A', '8A', '0G', '07', '18', '37', '43'
        # 3. terms_freq != 'D'
        # 4. terms_dur != 'REV'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'R', 'acct_type':'2A', 'terms_freq':'M',
                'terms_dur': 'LOC'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'R', 'acct_type':'8A', 'terms_freq':'P',
                'terms_dur': '001'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'0G', 'terms_freq':'O',
                'terms_dur': 'LOC'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'R', 'acct_type':'0A', 'terms_freq':'M',
                'terms_dur': '001'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'R', 'acct_type':'18', 'terms_freq':'D',
                'terms_dur': 'LOC'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'R', 'acct_type':'37', 'terms_freq':'P',
                'terms_dur': 'REV'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-terms_dur=REV

        self.assert_evaluator_correct(self.event, 'Type-TermsDuration-3', self.expected)

    def test_eval_type_terms_dur_4(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_type == '06', '18'
        # 3. terms_freq != 'D'
        # 4. int(terms_dur) > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'06', 'terms_freq':'M',
                'terms_dur': '1'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'P',
                'terms_dur': '2'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'C', 'acct_type':'06', 'terms_freq':'O',
                'terms_dur': '3'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'0A', 'terms_freq':'M',
                'terms_dur': '4'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'D',
                'terms_dur': '5'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'06', 'terms_freq':'P',
                'terms_dur': '0'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'06', 'terms_freq':'P',
                'terms_dur': 'REV'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'06', 'terms_freq':'P',
                'terms_dur': '***'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:NO-port_type=C, 35: NO-acct_type=0A,
        # 36: NO-terms_freq=D, 37: NO-terms_dur=0, 37: NO-terms_dur=REV

        self.assert_evaluator_correct(self.event, 'Type-TermsDuration-4', self.expected)