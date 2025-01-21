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
        # 1. acct_type == '0A', '0C', '0F', '2C', '5A', '5B', '6A', '6B', '6D', 
        #                 '7B', '9A', '01', '02', '03', '04', '05', '06', '08',
        #                 '10', '11', '13', '17', '19', '20', '25', '26', '47',
        #                 '48', '77', '91'
        # 2. terms_freq != 'D'
        # 3. credit_limit > 0

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
                'port_type':'M', 'acct_type':'08', 'terms_freq':'M',
                'credit_limit': 25
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'M', 'acct_type':'19', 'terms_freq':'P',
                'credit_limit': 20
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'0C', 'terms_freq':'M',
                'credit_limit': 25
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'48', 'terms_freq':'P',
                'credit_limit': 20
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'9B', 'terms_freq':'M',
                'credit_limit': 10
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'port_type':'I', 'acct_type':'6D', 'terms_freq':'D',
                'credit_limit': 5
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'port_type':'I', 'acct_type':'0F', 'terms_freq':'P',
                'credit_limit': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT, 36: HIT, 37: HIT, 
        # 38: NO-acct_type=9B, 39: NO-terms_freq=D, 40: NO-credit_limit=0

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'},
            {'id': 37, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0037'}]

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-1', expected)

    def test_eval_type_credit_limit_2(self):
        # Hits when all conditions are met:
        # 1. acct_type == '0G', '2A', '7A', '8A', '9B', '07',
        #                 '15', '18', '37', '43', '47', '89'
        # 2. terms_freq != 'D'
        # 3. credit_limit == 0

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
                'port_type':'O', 'acct_type':'2A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'8A', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'R', 'acct_type':'2A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'R', 'acct_type':'8A', 'terms_freq':'P',
                'credit_limit': 0
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'18', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'port_type':'C', 'acct_type':'0A', 'terms_freq':'M',
                'credit_limit': 0
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'port_type':'C', 'acct_type':'43', 'terms_freq':'D',
                'credit_limit': 0
            }, {
                'id': 41, 'activity_date': acct_date, 'cons_acct_num': '0041',
                'port_type':'C', 'acct_type':'47', 'terms_freq':'P',
                'credit_limit': 10
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT, 36: HIT, 37: HIT, 38: HIT,
        # 39: NO-acct_type=0A, 40: NO-terms_freq=D, 41: NO-credit_limit=10

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'},
            {'id': 37, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0037'},
            {'id': 38, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0038'}]

        self.assert_evaluator_correct(self.event, 'Type-CreditLimit-2', expected)

    def test_eval_type_hcola_1(self):
        # Hits when all conditions are met:
        # 1. acct_type == '00', '0A', '0C', '0F', '2C', '3A', '5A',
        #                 '5B', '6A', '6B', '6D', '7B', '9A', '01',
        #                 '02', '03', '04', '05', '06', '08', '10',
        #                 '11', '13', '17', '19', '20', '25', '26',
        #                 '47', '48', '77', '91'
        # 2. terms_freq != 'D'
        # 3. hcola <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'I', 'acct_type':'00', 'hcola': -1, 'terms_freq': 'P'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'M', 'acct_type':'08', 'hcola': -1, 'terms_freq': 'W'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'O', 'acct_type':'0C', 'hcola': -1, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'I', 'acct_type':'12', 'hcola': -5, 'terms_freq': 'P'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_type':'91', 'hcola': -5, 'terms_freq': 'D'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'I', 'acct_type':'00', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'3A', 'hcola': 5, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-acct_type=12, 36: NO-terms_freq=D,
        # 37: HIT, 38: NO-hcola=5

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 37, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0037'}
        ]

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-1', expected)

    def test_eval_type_hcola_2(self):
        # Hits when all conditions are met:
        # 1. acct_type == '0G', '2A', '7A', '8A', '9B', '07',
#                         '15', '18', '37', '43', '47', '89'
        # 2. terms_freq != 'D'
        # 3. hcola == 0
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
                'port_type':'R', 'acct_type':'0G', 'hcola': 0, 'terms_freq': 'P'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'acct_type':'9B', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'O', 'acct_type':'77', 'hcola': 0, 'terms_freq': 'W'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'O', 'acct_type':'37', 'hcola': 0, 'terms_freq': 'D'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'O', 'acct_type':'2A', 'hcola': 10, 'terms_freq': 'P'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT,
        # 36: NO-acct_type=77, 37: NO-terms_freq=D, 
        # 38: NO-hcola=10

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'}
        ]

        self.assert_evaluator_correct(self.event, 'Type-HCOLA-2', expected)

    def test_type_smpa_1(self):
        # Hits when all conditions are met:
        # 1. port_type == 'I'
        # 2. acct_stat == '11'
        # 3. spc_com_cd == 'BS'
        # 4. smpa > 0

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
                'port_type':'I', 'acct_stat':'11', 'acct_type':'07',
                'spc_com_cd': 'BS', 'smpa': 5
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'C', 'acct_stat':'11', 'acct_type':'02',
                'spc_com_cd': 'BS', 'smpa': 15
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'I', 'acct_stat':'05', 'acct_type':'03',
                'spc_com_cd': 'BS', 'smpa': 10
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
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-port_type=C, 
        # 36: NO-acct_stat=5, 37: NO-spc_com_cd=AU, 38: NO-smpa=0

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}]

        self.assert_evaluator_correct(self.event, 'Type-SMPA-1', expected)

    def test_eval_type_terms_dur_1(self):
    # Hits when the following condition is met...
    #     1. terms_freq != 'D'

    # ... AND one of the following sets of conditions
    #     a. port_type == 'C' & terms_dur != 'LOC'
    #     b. port_type == 'O' & terms_dur != '001'
    #     c. port_type == 'R' & terms_dur != 'REV'
    #     d. port_type == 'I' & int(terms_dur) <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': 'REV'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': '001'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type':'O', 'acct_type':'9B', 'terms_freq':'P',
                'terms_dur': 'LOC'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type':'O', 'acct_type':'9B', 'terms_freq':'P',
                'terms_dur': '12'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type':'R', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': 'LOC'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type':'R', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': '001'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type':'I', 'acct_type':'06', 'terms_freq':'M',
                'terms_dur': 'REV'
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'port_type':'I', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': '000'
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'port_type':'I', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': '0'
            }, {
                'id': 41, 'activity_date': acct_date, 'cons_acct_num': '0041',
                'port_type':'I', 'acct_type':'15', 'terms_freq':'O',
                'terms_dur': '-1'
            }, {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0042',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'D',
                'terms_dur': 'REV'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0043',
                'port_type':'C', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': 'LOC'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0044',
                'port_type':'O', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': '001'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0045',
                'port_type':'R', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': 'REV'
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0046',
                'port_type':'I', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': '12'
            }, {
                'id': 47, 'activity_date': acct_date, 'cons_acct_num': '0047',
                'port_type':'I', 'acct_type':'7A', 'terms_freq':'M',
                'terms_dur': '001'
            }
            ]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT, 36: HIT,
        # 37: HIT, 38: HIT, 39: HIT, 40: HIT, 41: HIT,
        # 42: NO-terms_freq=D, 43: NO-port_type=C & terms_dur=LOC,
        # 44: NO-port_type=O & terms_dur=001, 45: NO-port_type=R & terms_dur=REV,
        # 46: NO-port_type=I & terms_dur=12, 47: NO-port_type=I & terms_dur=001

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'},
            {'id': 37, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0037'},
            {'id': 38, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0038'},
            {'id': 39, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0039'},
            {'id': 40, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0040'},
            {'id': 41, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0041'}]


        self.assert_evaluator_correct(self.event, 'Type-TermsDuration-1', expected)
