from django.test import TestCase

from datetime import date
from parse_m2.initiate_post_parsing import associate_previous_records
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
    l1_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class ProgEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()

        self.prev_data_file = M2DataFile(event=self.event, file_name='old_file.txt')
        self.prev_data_file.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        self.expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 43, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'}
        ]

    def create_prog_account_change_activity(self, prev_l1_segments, l1_segments):
        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032'},
            {'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033'},
            {'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034'},
            {'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035'}]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)
        for s in prev_l1_segments:
            l1_record(s)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032'},
            {'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033'},
            {'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034'},
            {'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035'}]
        for r in activities:
            acct_record(self.data_file, r)
        for s in l1_segments:
            l1_record(s)
        associate_previous_records(self.event)

    ############################
    # Tests for the category prog evaluators

    def test_eval_prog_account_change_1(self):
    # Hits when both conditions met:
    # 1. previous_values__l1__change_ind == '1', '3'
    # 2. l1__new_acc_num == previous_values__l1__new_acc_num

        # Create L1 segment data
        prev_l1_segments = [
            {'id': 32, 'change_ind': '1', 'new_acc_num': '032'},
            {'id': 33, 'change_ind': '3', 'new_acc_num': '033'},
            {'id': 34, 'change_ind': '2', 'new_acc_num': '034'},
            {'id': 35, 'change_ind': '3', 'new_acc_num': '035'}]

        l1_segments = [
            {'id': 42, 'change_ind': '1', 'new_acc_num': '032'},
            {'id': 43, 'change_ind': '3', 'new_acc_num': '033'},
            {'id': 44, 'change_ind': '1', 'new_acc_num': '034'},
            {'id': 45, 'change_ind': '3', 'new_acc_num': '0035'}]

        # Create Account Activities data
        self.create_prog_account_change_activity(prev_l1_segments, l1_segments)
        # 42: HIT, 43: HIT, 44: NO-previous_values__l1__change_ind=2,
        # 45: NO-l1__new_acc_num != previous_values__l1__new_acc_num

        self.assert_evaluator_correct(self.event, 'PROG-AccountChange-1', self.expected)

    def test_eval_prog_account_change_2(self):
    # Hits when both conditions met:
    # 1. previous_values__l1__change_ind == '2', '3'
    # 2. l1__new_id_num == previous_values__l1__new_id_num

        # Create L1 segment data
        prev_l1_segments = [
            {'id': 32, 'change_ind': '2', 'new_id_num': '1'},
            {'id': 33, 'change_ind': '3', 'new_id_num': '2'},
            {'id': 34, 'change_ind': '1', 'new_id_num': '3'},
            {'id': 35, 'change_ind': '2', 'new_id_num': '4'}]

        l1_segments = [
            {'id': 42, 'change_ind': '1', 'new_id_num': '1'},
            {'id': 43, 'change_ind': '2', 'new_id_num': '2'},
            {'id': 44, 'change_ind': '3', 'new_id_num': '3'},
            {'id': 45, 'change_ind': '1', 'new_id_num': '1'}]

        # Create Account Activities data
        self.create_prog_account_change_activity(prev_l1_segments, l1_segments)
        # 42: HIT, 43: HIT, 44: NO-previous_values__l1__change_ind=1,
        # 45: NO-l1__new_id_num != previous_values__l1__new_id_num

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-AccountChange-2', self.expected)

    def test_eval_prog_dofd_1(self):
    # Hits when all conditions met:
    # 1. previous_values__acct_stat == '61', '62', '63', '64', '65', '71',
    #                 '78', '80' '82', '83', '84', '88', '89', '94', '95',
    #                 '96', '93', '97'
    # 2. acct_stat == '61', '62', '63', '64', '65', '71', '78', '80','82',
    #                 '83', '84', '88', '89', '94', '95', '96', '93', '97'
    # 2. previous_values__dofd != dofd

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'61', 'dofd': None
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62', 'dofd': date(2019, 11, 1)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'66', 'dofd': None
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'71', 'dofd': date(2019, 10, 31)
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'dofd': None
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)


        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'61', 'dofd': date(2019, 12, 1)
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62', 'dofd': date(2019, 12, 10)
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'63', 'dofd': date(2019, 10, 31)
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'77', 'dofd': None
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'dofd': None
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=66,
        # 45: NO-acct_stat=77, 46: No-previous_values__dofd == dofd

        self.assert_evaluator_correct(self.event, 'PROG-DOFD-1', self.expected)

    def test_eval_prog_dofd_3(self):
    # Hits when all conditions met:
    # 1. previous_values__acct_stat == '71', '78', '80', '82', '83', '84', '61', '62',
    #                                  '63', '64', '65', '93', '94', '95', '96', '97'
    # 2. acct_stat == '11'
    # 3. previous_values__dofd == dofd

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'61', 'dofd': None
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62', 'dofd': date(2019, 11, 1)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'66', 'dofd': None
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'71', 'dofd': date(2019, 10, 31)
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'acct_stat':'78', 'dofd': None
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'dofd': None
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'11', 'dofd': date(2019, 11, 1)
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'11', 'dofd': None
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'77', 'dofd': date(2019, 10, 31)
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'11', 'dofd': date(2019, 10, 31)
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=66,
        # 45: NO-acct_stat=77, 46: No-previous_values__dofd != dofd

        self.assert_evaluator_correct(self.event, 'PROG-DOFD-3', self.expected)