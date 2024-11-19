from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
    k2_record,
    l1_record
)
from parse_m2.models import Metro2Event, M2DataFile


class SCCEvalsTestCase(TestCase, EvaluatorTestHelper):
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

    def create_data(self, activities: dict):
        for item in activities:
            acct_record(self.data_file, item)
        # Create the segment data
        self.create_bulk_k2()

    def create_bulk_k2(self):
        # Create the segment data
        k2_segments = [
            {'id': 32, 'purch_sold_ind': 'a', 'purch_sold_name': 'hit'},
            {'id': 34, 'purch_sold_ind': '2', 'purch_sold_name': ''},
            {'id': 35, 'purch_sold_ind': 'c', 'purch_sold_name': 'no2'}
        ]
        for item in k2_segments:
            k2_record(item)

    def create_other_segments(self):
        # Create the other segment data
        self.l1 = l1_record({'id':32})
        self.l1.save()

    ############################
    # Tests for the category SCC evaluators
    def test_eval_scc_acct_change_1(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'O'
        # 2. L1.change_ind != '1', '2', '3'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'spc_com_cd': 'O'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'spc_com_cd': 'O'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'spc_com_cd': 'BC'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'spc_com_cd': 'O',
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-spc_com_cd=BC, 35: NO-L1.change_ind=1


        # Create the segment data
        l1_segments = [
            {'id': 32, 'change_ind': ''},
            {'id': 35, 'change_ind': '1'}
        ]
        for item in l1_segments:
            l1_record(item)

        self.assert_evaluator_correct(self.event, 'SCC-AccountChange-1', self.expected)

    def test_eval_scc_apd_1(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AU', 'AX', 'BP', 'C', 'AH', 'AT',
        #                  'O', 'BC', 'BF', 'BJ', 'AS'
        # 2. amt_past_due > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'amt_past_due': 200, 'current_bal': 0,
                'spc_com_cd': 'C'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'amt_past_due': 9, 'current_bal': 9,
                'spc_com_cd': 'BF'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'71', 'amt_past_due': 20, 'current_bal': 0,
                'spc_com_cd': 'WT'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'65', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'AU'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'65', 'amt_past_due': -30, 'current_bal': 0,
                'spc_com_cd': 'AS'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-spc_com_cd=WT, 35: NO-amt_past_due=0

        self.assert_evaluator_correct(self.event, 'SCC-APD-1', self.expected)

    def test_eval_scc_apd_2(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BD', 'BG', 'BI', 'BK', 'BA', 'BO'
        # 2. amt_past_due <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'acct_type': '08', 'amt_past_due': -200,
                'current_bal': 0, 'spc_com_cd': 'BD'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'acct_type': '26', 'amt_past_due': 0,
                'current_bal': 9, 'spc_com_cd': 'BA'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'acct_type': '26', 'amt_past_due': 0,
                'current_bal': 9, 'spc_com_cd': 'BO'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'71', 'acct_type': '0', 'amt_past_due': -1,
                'current_bal': 10, 'spc_com_cd': 'AI'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'65', 'acct_type': '0', 'amt_past_due': 1,
                'current_bal': 100, 'spc_com_cd': 'BG'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: HIT, 35: NO-spc_com_cd=AI, 36: NO-amt_past_due=1

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}
        ]
        self.assert_evaluator_correct(self.event, 'SCC-APD-2', expected)

    def test_eval_scc_balance_1(self):
        # Hits when both conditions met:
        # spc_com_cd == 'AU', 'AX', 'BP', 'C', 'AH', 'AT',
        #               'O', 'BC', 'BF', 'BJ', 'AS'
        # 2. current_bal > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'amt_past_due': 0, 'current_bal': 200,
                'spc_com_cd': 'C'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'amt_past_due': 9, 'current_bal': 100,
                'spc_com_cd': 'BF'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'amt_past_due': 9, 'current_bal': -9,
                'spc_com_cd': 'AX'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'71', 'amt_past_due': 0, 'current_bal': 100,
                'spc_com_cd': 'WT'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'65', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'AU'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-current_bal<0, 35:NO-spc_com_cd=WT, 
        # 36: NO-current_bal=0

        self.assert_evaluator_correct(self.event, 'SCC-Balance-1', self.expected)

    def test_eval_scc_balance_2(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'BD', 'BG', 'BI', 'BK', 'CP', 'BA', 'BO'
        # 2. current_bal <= 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'acct_type': '08', 'amt_past_due': 200,
                'current_bal': -1, 'spc_com_cd': 'BD'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'acct_type': '26', 'amt_past_due': 9,
                'current_bal': 0, 'spc_com_cd': 'BA'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'71', 'acct_type': '0', 'amt_past_due': 0,
                'current_bal': -1, 'spc_com_cd': 'AI'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'65', 'acct_type': '0', 'amt_past_due': 0,
                'current_bal': 5, 'spc_com_cd': 'BG'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-spc_com_cd=AI, 35: NO-current_bal=5

        self.assert_evaluator_correct(self.event, 'SCC-Balance-2', self.expected)

    def test_eval_scc_dateclosed_1(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'BO', 'CP'
        # 2. date_closed != None

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'spc_com_cd': 'BO', 'date_closed': date(2019, 12, 31)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'spc_com_cd': 'CP', 'date_closed': date(2019, 12, 31)
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'spc_com_cd': 'BO', 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'spc_com_cd': 'BC', 'date_closed': date(2019, 12, 31)
            }]
        self.create_data(activities)
        # 32: HIT, # 33: HIT, 34: No-DateClosed=None, 35: NO-spc_com_cd=BC        

        self.assert_evaluator_correct(self.event, 'SCC-DateClosed-1', self.expected)


    def test_eval_scc_dateclosed_2(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'M'
        # 2. date_closed == None

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'spc_com_cd': 'M', 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'spc_com_cd': 'M', 'date_closed': date(2019, 12, 31)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'spc_com_cd': 'BC', 'date_closed': None
            }]
        self.create_data(activities)
        # 32: HIT, 34: No-DateClosed != None, 35: NO-spc_com_cd=BC

        # Create the segment data
        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, 'SCC-DateClosed-2', expected)

    def test_eval_scc_purchase_sold_1_func(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AH'
        # 2. k2__purch_sold_ind != '2'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'spc_com_cd': 'AH'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'spc_com_cd': 'AH'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'spc_com_cd': 'AH'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'spc_com_cd': 'WT'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-k2__purch_sold_ind=2, 35: NO-spc_com_cd=WT,

        self.assert_evaluator_correct(self.event, 'SCC-PurchasedSold-1', self.expected)

    def test_eval_scc_purchase_sold_2_func(self):
        # Hits when both conditions met:
        # 1. spc_com_cd == 'AH'
        # 2. k2__purch_sold_name == ''

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'spc_com_cd': 'AH'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'spc_com_cd': 'AH'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'spc_com_cd': 'AH'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'spc_com_cd': 'WT'
            }]
        self.create_data(activities)
        # 32: NO-k2__purch_sold_name='hit', 33: NO-k2__purch_sold_name=None,
        # 34: HIT,35: NO-spc_com_cd=WT,

        # Create the segment data
        expected = [
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'}
        ]

        self.assert_evaluator_correct(self.event, 'SCC-PurchasedSold-2', expected)

    def test_eval_scc_status_1(self):
        # Hits when one of the following sets of conditions met:
        # 1. spc_com_cd == 'BC', 'BF' & acct_stat != '13'
        # 2. spc_com_cd == 'AU', 'AX', 'BP', 'C' & 
        #       acct_stat != '13', '61', '62', '63', '64', '65'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'C'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'amt_past_due': 9, 'current_bal': 9,
                'spc_com_cd': 'AX'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'89', 'amt_past_due': 9, 'current_bal': 9,
                'spc_com_cd': 'BC'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'amt_past_due': 9, 'current_bal': 9,
                'spc_com_cd': 'BF'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'71', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'WT'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'65', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'AU'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'13', 'amt_past_due': 0, 'current_bal': 0,
                'spc_com_cd': 'BC'
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT,
        # 36: NO-spc_com_cd=WT, 37: NO-acct_stat=65, 38: NO-acct_stat=13

        # Create the segment data
        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'}
        ]

        self.assert_evaluator_correct(self.event, 'SCC-Status-1', expected)

    def test_eval_scc_status_2(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'AP', 'BD', CP'
        # 2. acct_stat == '13', '61', '62', '63', '64', '65'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'spc_com_cd': 'CP'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'61', 'spc_com_cd': 'CP'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'62', 'spc_com_cd': 'AP'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'65', 'spc_com_cd': 'BD'
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'97', 'spc_com_cd': 'AP'
            }, {
                'id': 37, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'11', 'spc_com_cd': 'CP'
            }, {
                'id': 38, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'62', 'spc_com_cd': 'CK',
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: HIT, 35: HIT,
        # 36: NO-acct_stat=97, 37: NO-acct_stat=11, 38: NO-spc_com_cd=CK

        # Create the segment data
        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'}
        ]

        self.assert_evaluator_correct(self.event, 'SCC-Status-2', expected)

    def test_eval_scc_status_3(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'BA'
        # 2. acct_stat != '71', '78', '80', '82', '83', '84', '88',
        #                 '89', '93', '94', '95', '96', '97'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'08', 'spc_com_cd': 'BA'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'26', 'spc_com_cd': 'BA'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'71', 'spc_com_cd': 'BA'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'0G', 'spc_com_cd': 'BC',
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'95', 'spc_com_cd': 'BA',
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=71, 35: NO-spc_com_cd=BC,
        # 36: NO-acct_stat=95

        self.assert_evaluator_correct(self.event, 'SCC-Status-3', self.expected)

    def test_eval_scc_status_4(self):
        # hits when both conditions met:
        # 1. spc_com_cd == 'BO'
        # 2. acct_stat == '13', '61', '62', '63', '64',
        #                 '65', '88', '89', '94'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'spc_com_cd': 'BO'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'61', 'spc_com_cd': 'BO'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'0G', 'spc_com_cd': 'BO'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'spc_com_cd': 'BC',
            }]
        self.create_data(activities)
        # 32: HIT, 33: HIT, 34: NO-acct_stat=OG, 35: NO-spc_com_cd=BC

        self.assert_evaluator_correct(self.event, 'SCC-Status-4', self.expected)
