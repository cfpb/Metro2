from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class StatusEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        self.expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}]


    ############################
    # Tests for the category Status evaluators

    def test_eval_status_apd_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05','11','13','61','62','63','64','65'
    # 2. amt_past_due > 0

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

        self.assert_evaluator_correct(
            self.event, 'Status-APD-1', self.expected)

    def test_eval_status_apd_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '71','78','80','82','83','84','93','97'
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
                'acct_stat':'82', 'compl_cond_cd':'XB', 'amt_past_due': 1
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=79,
        # 35: NO-amt_past_due > 0

        self.assert_evaluator_correct(
            self.event, 'Status-APD-2', self.expected)

    def test_eval_status_apd_3(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '95','96'
    # 2. acct_type == '00', '13', '3A'
    # 3. port_type == 'I'
    # 4. amt_past_due == 0

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

        self.assert_evaluator_correct(self.event, 'Status-APD-3', self.expected)

    def test_eval_status_balance_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05','13','61','62','63','64','65'
    # 2. current_bal > 0

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

        self.assert_evaluator_correct(self.event, 'Status-Balance-1', self.expected)

    def test_eval_status_balance_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '71', '78', '80', '82', '83', '84', '93', '97'
    # 2. current_bal == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'current_bal':0,
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'78', 'current_bal':0,
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'79', 'current_bal':0,
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80', 'current_bal':10,
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=79, 35: NO-current_bal=10,

        self.assert_evaluator_correct(self.event, 'Status-Balance-2', self.expected)

    def test_eval_status_balance_3(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '95', '96'
    # 2. current_bal == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'95', 'current_bal':0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'96',  'current_bal':0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'94',  'current_bal':0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'95', 'current_bal': 5
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=94,
        # 35: NO-current_bal=5

        self.assert_evaluator_correct(self.event, 'Status-Balance-3', self.expected)

    def test_eval_status_balance_4(self):
    # Hits when all conditions are met:
    # 1. port_type == 'I', 'M'
    # 2. acct_stat == 11
    # 3. spc_com_cd != 'BS'
    # 4. compl_cond_cd != 'XA'
    # 5. current_bal == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'I', 'acct_stat':'11', 'current_bal': 0, 'spc_com_cd': 'M',
                'compl_cond_cd': 'XB'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'M', 'acct_stat':'11', 'current_bal': 0, 'spc_com_cd': 'BB',
                'compl_cond_cd': 'O'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'R', 'acct_stat':'11', 'current_bal': 0, 'spc_com_cd': 'BB',
                'compl_cond_cd': 'XB'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'M', 'acct_stat':'11', 'current_bal': 5, 'spc_com_cd': 'BB',
                'compl_cond_cd': 'XB'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'M', 'acct_stat':'13', 'current_bal': 0, 'spc_com_cd': 'BB',
                'compl_cond_cd': 'XB'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'M', 'acct_stat':'11', 'current_bal': 0, 'spc_com_cd': 'BS',
                'compl_cond_cd': 'XB'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type': 'M', 'acct_stat':'11', 'current_bal': 0, 'spc_com_cd': 'BB',
                'compl_cond_cd': 'XA'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=R,
        # 35: NO-current_bal=5, 36: NO-acct_stat=13,
        # 37: NO-spc_com_cd='BS', 38: NO-compl_cond_cd='XA'

        self.assert_evaluator_correct(self.event, 'Status-Balance-4', self.expected)

    def test_eval_status_balance_5(self):
    # Hits when all conditions are met:
    # 1. acct_stat == 11
    # 2. current_bal == 0
    #
    # ... AND one of the following sets of conditions is met:
    #     a. port_type == 'C' & acct_type == '15','43','47','89','7A','9B'
    #     b. port_type == 'O', 'R' & acct_type == '18','37','43','2A','8A'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'C', 'acct_type': '15', 'acct_stat':'11', 'current_bal': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'R', 'acct_type': '43', 'acct_stat':'11', 'current_bal': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'M', 'acct_type': '43', 'acct_stat':'11', 'current_bal': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'R', 'acct_type': '43', 'acct_stat':'11', 'current_bal': 5
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'C', 'acct_type': '15', 'acct_stat':'13', 'current_bal': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'C', 'acct_type': '01', 'acct_stat':'11', 'current_bal': 0
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'port_type': 'O', 'acct_type': '89', 'acct_stat':'11', 'current_bal': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=M,
        # 35: NO-current_bal=5, 36: NO-acct_stat=13,
        # 37: NO-acct_type=01, 38: NO- port_type=O & acct_type=89

        self.assert_evaluator_correct(self.event, 'Status-Balance-5', self.expected)


    def test_eval_status_balance_6(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '88', '89'
    # 3. current_bal == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89', 'current_bal': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'88', 'current_bal': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'13', 'current_bal': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'11', 'current_bal': 5
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=13,
        # 35: NO-current_bal=5

        self.assert_evaluator_correct(self.event, 'Status-Balance-6', self.expected)

    def test_eval_status_balance_7(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '94'
    # 2. pmt_rating == '1', '2', '3', '4', '5', '6', 'G', 'L'
    # 3. current_bal == 0
    # 4. compl_cond_cd != 'XA'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'94', 'pmt_rating': 'L', 'current_bal': 0, 'compl_cond_cd': 'XB'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'94', 'pmt_rating': '1', 'current_bal': 0, 'compl_cond_cd': 'XB'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'13', 'pmt_rating': '1', 'current_bal': 0, 'compl_cond_cd': 'XB'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'94', 'pmt_rating': '1', 'current_bal': 5, 'compl_cond_cd': 'XB'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'94', 'pmt_rating': '0', 'current_bal': 0, 'compl_cond_cd': 'XB'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'94', 'pmt_rating': '1', 'current_bal': 0, 'compl_cond_cd': 'XA'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=13,
        # 35: NO-current_bal=5, 36: NO-pmt_rating=0,
        # 37: NO-compl_cond_cd=XA

        self.assert_evaluator_correct(self.event, 'Status-Balance-7', self.expected)

    def test_eval_status_balance_8(self):
        # Hits when all conditions are met:
        # 1. port_type == 'M' OR port_type == 'I'
        # 2. current_bal == 0
        # 3. l1_change_ind == None
        # 4. spc_com_cd != 'AH', 'AT', 'O', 'BB', 'BE'
        # 5. acct_stat != '13', '62', '64', 'DA', 'DF'
        #
        # ... AND the following set of conditions is NOT met
        # a. port_type='I' & acct_stat == '61', '63', '88', '95', '96'
        # b. port_type='M' & acct_stat == '65', '94'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'M', 'acct_stat':'11', 'spc_com_cd': 'AB', 'current_bal': 0,
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'I', 'acct_stat':'05', 'spc_com_cd': 'M', 'current_bal': 0,
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'R', 'acct_stat':'11', 'spc_com_cd': 'F', 'current_bal': 0,
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'M', 'acct_stat':'05', 'spc_com_cd': 'AB', 'current_bal': 5,
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'I', 'acct_stat':'11', 'spc_com_cd': 'AH', 'current_bal': 0,
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'M', 'acct_stat':'13', 'spc_com_cd': 'AB', 'current_bal': 0,
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=R,
        # 35: NO-current_bal=5, 36: NO-spc_com_cd=AH,
        # 37: NO-acct_stat=13

        self.assert_evaluator_correct(self.event, 'Status-Balance-8', self.expected)

    def test_eval_status_balance_9(self):
        # Hits when all following conditions are met:
        # 1. port_type == 'C', 'O', 'R'
        # 2. current_bal == 0
        # 3. l1_change_ind == None
        # 4. spc_com_cd != 'AH', 'AT', 'O'
        # 5. acct_stat != '11', '13', '62', '64', 'DA', 'DF'

        # ... AND none of the following sets of conditions is met
        #  a. port_type='C', acct_stat == '65', '88', '89', '94'
        #  b. port_type='O', acct_stat == '88'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AB', 'current_bal': 0,
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'R', 'acct_stat':'93', 'spc_com_cd': 'M', 'current_bal': 0,
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'M', 'acct_stat':'05', 'spc_com_cd': 'F', 'current_bal': 0,
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AB', 'current_bal': 33,
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AH', 'current_bal': 0,
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'C', 'acct_stat':'13', 'spc_com_cd': 'AB', 'current_bal': 0,
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=M,
        # 35: NO-current_bal=33, 36: NO-spc_com_cd=AH,
        # 37: NO-acct_stat=13

        self.assert_evaluator_correct(self.event, 'Status-Balance-9', self.expected)

    def test_eval_status_balance_10(self):
        # Hits when all conditions are met:
        # 1. current_bal > 0
        # 2. l1_change_ind == None
        # 3. spc_com_cd != 'AH', 'AT', 'O'
        # 4. acct_stat != '11', '71', '78', '80', '82', '83',
        #                 '84','93', '97', 'DA', 'DF'
        #
        # ... AND none of the following sets of conditions is met
        #  a. port_type == 'I' & acct_stat = '95', '96'
        #  b. port_type == 'O' & acct_stat = '88'
        #  c. port_type == 'C', 'M' &  acct_stat = '88', '89', '94'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AB', 'current_bal': 300,
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'R', 'acct_stat':'95', 'spc_com_cd': 'M', 'current_bal': 500,
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AB', 'current_bal': 0,
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AH', 'current_bal': 500,
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'port_type': 'C', 'acct_stat':'05', 'spc_com_cd': 'AH', 'current_bal': 500,
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'port_type': 'C', 'acct_stat':'88', 'spc_com_cd': 'AB', 'current_bal': 1,
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34:  NO-current_bal=0,
        # 35: NO-spc_com_cd=AH, 36: NO-acct_stat=11
        # 37: NO-port_type=c & acct_stat=88

        self.assert_evaluator_correct(self.event, 'Status-Balance-10', self.expected)

    def test_eval_status_chargeoff_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05', '11', '13', '62', '65', '71', '78',
    #                 '80', '82', '83', '84', '89', '93'
    # 2. orig_chg_off_amt > 0

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

        self.assert_evaluator_correct(self.event, 'Status-ChargeOff-1', self.expected)

    def test_eval_status_chargeoff_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '64', '97'
    # 2. orig_chg_off_amt == 0

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

        self.assert_evaluator_correct(self.event, 'Status-ChargeOff-2', self.expected)

    def test_eval_status_date_closed_1(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '05', '13', '62', '64', '65'
    # 2. date_closed == None

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

        self.assert_evaluator_correct(self.event, 'Status-DateClosed-1', self.expected)

    def test_eval_status_date_closed_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '11','71','78','80','82','83','84','93', '97'
    # 2. compl_cond_cd != 'XA'
    # 3. date_closed != None

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
                'acct_stat':'97',  'compl_cond_cd': 'XD', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'12',  'compl_cond_cd': 'XD', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1)
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'80', 'compl_cond_cd': 'XE', 'date_closed': None
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-acct_stat=12,
        # 35: NO-compl_cond_cd=XA, 36: No-date_closed=None

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}]

        self.assert_evaluator_correct(self.event, 'Status-DateClosed-2', expected)

    def test_eval_status_date_closed_3(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '89', '94'
    # 2. date_closed == None

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'94', 'date_closed':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'01', 'date_closed':None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'89', 'date_closed':date(2019, 12, 31)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=01, 35: NO-date_closed!=None

        self.assert_evaluator_correct(self.event, 'Status-DateClosed-3', self.expected)

    def test_eval_status_dofd_1(self):
    # Hits when the following condition is met:
    # 1. dofd == None

    # ...AND one of the following conditions is met:
    # a. acct_stat == '61', '62', '63', '64', '65', '71', '78', '80','82',
    #                 '83', '84', '88', '89', '94', '95', '96', '93', '97'
    # b. acct_stat == '05', '13' & pmt_rating == '1', '2', '3', '4', '5',
    #                                            '6', 'G', 'L'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'pmt_rating':'0', 'acct_stat':'71', 'dofd':None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'pmt_rating':'1', 'acct_stat':'97', 'dofd':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'pmt_rating':'1', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'pmt_rating':'G', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'pmt_rating':'1', 'acct_stat':'13', 'dofd':None
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'pmt_rating':'2', 'acct_stat':'13', 'dofd':None
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'pmt_rating':'3', 'acct_stat':'11', 'dofd':None
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'pmt_rating':'7', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'pmt_rating':'0', 'acct_stat':'13', 'dofd':None
            }, {
                'id': 41, 'activity_date': acct_date, 'cons_acct_num': '0041',
                'pmt_rating':'0', 'acct_stat':'65', 'dofd':date(2019, 12, 31)
            }, {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0042',
                'pmt_rating':'1', 'acct_stat':'05', 'dofd':date(2019, 12, 31)
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0043',
                'pmt_rating':'L', 'acct_stat':'13', 'dofd':date(2019, 12, 31)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT, 36: HIT, 37: HIT,
        # 38: NO-acct_stat=11, 39: NO-pmt_rating=7,
        # 40: NO-pmt_rating=0, 41: NO-dofd=date(2019, 12, 31),
        # 42: NO-dofd=date(2019, 12, 31), 43: NO-dofd=date(2019, 12, 31)

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'},
            {'id': 36, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0036'},
            {'id': 37, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0037'}]

        self.assert_evaluator_correct(self.event, 'Status-DOFD-1', expected)

    def test_eval_status_dofd_2(self):
    # Hits when the following condition is met:
    # 1. dofd != None
    # ... AND one of the following sets of conditions is met:
    #     a. acct_stat == '11'
    #     b. acct_stat == '05', '13' & pmt_rating == '0'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'pmt_rating':'0', 'acct_stat':'11', 'dofd':date(2019, 12, 31)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'pmt_rating':'0', 'acct_stat':'05', 'dofd':date(2019, 12, 31)
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'pmt_rating':'0', 'acct_stat':'13', 'dofd':date(2019, 12, 31)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'pmt_rating':'1', 'acct_stat':'11', 'dofd':date(2019, 12, 31)
            },  {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'pmt_rating':'3', 'acct_stat':'05', 'dofd':date(2019, 12, 31)
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'pmt_rating':'L', 'acct_stat':'13', 'dofd':date(2019, 12, 31)
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'pmt_rating':'0', 'acct_stat':'11', 'dofd':None
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'pmt_rating':'0', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'pmt_rating':'0', 'acct_stat':'13', 'dofd':None
            }, {
                'id': 41, 'activity_date': acct_date, 'cons_acct_num': '0041',
                'pmt_rating':'G', 'acct_stat':'11', 'dofd':None
            }, {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0042',
                'pmt_rating':'2', 'acct_stat':'05', 'dofd':None
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0043',
                'pmt_rating':'1', 'acct_stat':'13', 'dofd':None
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT,
        # 36: NO-pmt_rating=3, 37: NO-pmt_rating=L,
        # 38: NO-dofd=None, #39: NO-dofd=None,
        # 40: NO-dofd=None, #41: NO-dofd=None,
        # 42: NO-dofd=None, #43: NO-dofd=None,

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'}]
        self.assert_evaluator_correct(self.event, 'Status-DOFD-2', expected)

    def test_eval_status_payment_amount_1(self):
    # Hits when all conditions are met:
    # 1. port_type  == 'I', 'M'
    # 2. acct_stat == '11'
    # 3. terms_freq != 'D'
    # 4. date_open < (activity_date - 60 days)
    # 5. actual payment amount == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'port_type': 'I', 'date_open': date(2019, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'port_type': 'M', 'date_open': date(2019, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 0
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'port_type': 'I', 'date_open': date(2019, 10, 29),
                'terms_freq': 'D', 'actual_pmt_amt': 0
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'11', 'port_type': 'C', 'date_open': date(2019, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 0
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'01', 'port_type': 'M', 'date_open':date(2019, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 0
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'11', 'port_type': 'I', 'date_open':date(2019, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 1
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'11', 'port_type': 'M', 'date_open': date(2020, 10, 29),
                'terms_freq': '0', 'actual_pmt_amt': 0
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: No-term_freq=D, 35: NO-port_type=C,
        # 36: NO-acct_stat=01, #37: NO-act_pmt_amt=1,
        # 38: NO-date_open > (activity_date - 60 days)

        self.assert_evaluator_correct(self.event, 'Status-PaymentAmount-1', self.expected)

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

        self.assert_evaluator_correct(self.event, 'Status-SMPA-1', self.expected)

    def test_eval_status_smpa_2(self):
    # Hits when all conditions are met:
    # 1. acct_stat == '71', '78', '80', '82', '83', '84', '93'
    # 2. compl_cond_cd != 'XA'
    # 3. terms_freq != 'D'
    # 4. smpa == 0

    # ... AND at least one of the following sets of conditions
    # a. port_type == 'C'
    # b. acct_type == 15', '43', '47', '89', '7A', '9B'
    # OR
    # a. port_type == 'O', 'R'
    # b. acct_type == '18', '37', '43', '2A', '8A'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'acct_type':'15', 'port_type':'C',
                'compl_cond_cd': 'XB', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'78', 'acct_type':'43', 'port_type':'O',
                'compl_cond_cd': 'XC', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'80', 'acct_type':'18', 'port_type':'R',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'11', 'acct_type':'43', 'port_type':'R',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'80', 'acct_type':'43',  'port_type':'C',
                'compl_cond_cd': 'XA', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'83', 'acct_type':'43', 'port_type':'R',
                'compl_cond_cd': 'XB', 'smpa': 0, 'terms_freq': 'D'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'84', 'acct_type':'43', 'port_type':'C',
                'compl_cond_cd': 'XC', 'smpa': 1, 'terms_freq': '0'
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'acct_stat':'93', 'acct_type':'43', 'port_type':'I',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'acct_stat':'71', 'acct_type':'15', 'port_type':'R',
                'compl_cond_cd': 'XE', 'smpa': 0, 'terms_freq': '0'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-acct_stat=11, 36: NO-compl_cond_cd=XA,
        # 37: terms_freq=D, 38: smpa=1, # 39: acct_type=15 but port_type != C,
        # #40: port_type=R but acct_type != 15

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}, 
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}]

        self.assert_evaluator_correct(self.event, 'Status-SMPA-2', expected)

    def test_eval_status_smpa_3(self):
    # Hits when all conditions are met:
    # 1. port_type == 'I'
    # 3. acct_stat == '11', '71', '78', '80', '82', '83', '84', '93'
    # 3. compl_cond_cd != 'XA'
    # 4. spc_com_cd != 'BS'
    # 5. terms_freq != 'D'
    # 6. smpa == 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'acct_type':'00', 'port_type':'I',
                'compl_cond_cd': 'XB', 'smpa': 0, 'spc_com_cd': 'AH',
                'terms_freq': '0'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'acct_type':'01', 'port_type':'I',
                'compl_cond_cd': 'XC', 'smpa': 0, 'spc_com_cd': 'AT',
                'terms_freq': '0'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'78', 'acct_type':'02', 'port_type':'I',
                'compl_cond_cd': 'XD', 'smpa': 0, 'spc_com_cd': 'O',
                'terms_freq': '0'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80', 'acct_type':'0B',  'port_type':'R',
                'compl_cond_cd': 'XE', 'smpa': 0, 'spc_com_cd': 'BA',
                'terms_freq': '0'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'81', 'acct_type':'03', 'port_type':'I',
                'compl_cond_cd': 'XB', 'smpa': 0, 'spc_com_cd': 'DF',
                'terms_freq': '0'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'82', 'acct_type':'04', 'port_type':'I',
                'compl_cond_cd': 'XA', 'smpa': 0, 'spc_com_cd': 'BC',
                'terms_freq': '0'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'83', 'acct_type':'05', 'port_type':'I',
                'compl_cond_cd': 'XC', 'smpa': 0, 'spc_com_cd': 'BS',
                'terms_freq': '0'
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'acct_stat':'84', 'acct_type':'06', 'port_type':'I',
                'compl_cond_cd': 'XD', 'smpa': 0, 'spc_com_cd': 'BB',
                'terms_freq': 'D'
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'acct_stat':'93', 'acct_type':'10', 'port_type':'I',
                'compl_cond_cd': 'XE', 'smpa': 1, 'spc_com_cd': 'BA',
                'terms_freq': '0'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-port_type=R,
        # 36: NO-acct_stat=81, 37: compl_cond_cd=XA, 38: spc_com_cd=BS,
        # 39: terms_freq=D,  #40: smpa=1

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}, 
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}]

        self.assert_evaluator_correct(self.event, 'Status-SMPA-3', expected)

    def test_eval_status_smpa_4(self):
        # Hits when all conditions are met:
        # 1. acct_stat == '11'
        # 2. compl_cond_cd != 'XA'
        # 3. terms_freq != 'D'
        # 4. smpa == 0

        # ... AND at least one of the following sets of conditions
        # a. port_type == 'C'
        # b. acct_type == 15', '43', '47', '89', '7A', '9B'
        # OR
        # a. port_type == 'O', 'R'
        # b. acct_type == '18', '37', '43', '2A', '8A'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'acct_type':'15', 'port_type':'C',
                'compl_cond_cd': 'XB', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'acct_type':'43', 'port_type':'O',
                'compl_cond_cd': 'XC', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'acct_type':'18', 'port_type':'R',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80', 'acct_type':'43', 'port_type':'R',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'11', 'acct_type':'43',  'port_type':'C',
                'compl_cond_cd': 'XA', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'11', 'acct_type':'43', 'port_type':'R',
                'compl_cond_cd': 'XB', 'smpa': 0, 'terms_freq': 'D'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'11', 'acct_type':'43', 'port_type':'C',
                'compl_cond_cd': 'XC', 'smpa': 1, 'terms_freq': '0'
            }, {
                'id': 39, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'acct_stat':'93', 'acct_type':'43', 'port_type':'I',
                'compl_cond_cd': 'XD', 'smpa': 0, 'terms_freq': '0'
            }, {
                'id': 40, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'acct_stat':'11', 'acct_type':'15', 'port_type':'R',
                'compl_cond_cd': 'XE', 'smpa': 0, 'terms_freq': '0'
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-acct_stat=80, 36: NO-compl_cond_cd=XA,
        # 37: terms_freq=D, 38: smpa=1, # 39: acct_type=15 but port_type != C,
        # #40: port_type=R but acct_type != 15

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}, 
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}]

        self.assert_evaluator_correct(self.event, 'Status-SMPA-4', expected)
        
