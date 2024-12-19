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

    def create_prog_account_change_activity(self, prev_l1_segments, l1_segments=[]):
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

    def test_eval_prog_account_change_3(self):
    # Hits when both conditions met:
    # 1. previous_values__l1__change_ind == '1', '3'
    # 2. previous_values__l1__new_acc_num == cons_acct_num


        # Create L1 segment data
        prev_l1_segments = [
            {'id': 32, 'change_ind': '1', 'new_acc_num': '0032'},
            {'id': 33, 'change_ind': '3', 'new_acc_num': '0033'},
            {'id': 34, 'change_ind': '2', 'new_acc_num': '0034'},
            {'id': 35, 'change_ind': '3', 'new_acc_num': '35'}]

        # Create Account Activities data
        self.create_prog_account_change_activity(prev_l1_segments)
        # 42: HIT, 43: HIT, 44: NO-previous_values__l1__change_ind=2,
        # 45: NO-previous_values__l1__new_acc_num != account_holder__cons_acct_num

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-AccountChange-3', self.expected)

    def test_eval_prog_bankruptcy_1(self):
    # Hits when both conditions met:
    # 1. previous_values__account_holder__cons_info_ind == 'V'
    # 2. account_holder__cons_info_ind == 'R'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'cons_info_ind':'V'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'cons_info_ind':'V'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'cons_info_ind':'R'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'cons_info_ind':'V'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'cons_info_ind':'R'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'cons_info_ind':'R'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'cons_info_ind':'R'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'cons_info_ind':'V'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__account_holder__cons_info_ind='R',
        # 45: NO-account_holder__cons_info_ind='V'

        self.assert_evaluator_correct(self.event, 'PROG-Bankruptcy-1', self.expected)

    def test_eval_prog_charge_off_1(self):
    # Hits when both conditions met:
    # 1. previous_values__acct_stat == '64', '97'
    # 2. previous_values__orig_chg_off_amt != orig_chg_off_amt

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'64', 'orig_chg_off_amt': 0
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97', 'orig_chg_off_amt': 5
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'66', 'orig_chg_off_amt': 10
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'97', 'orig_chg_off_amt': 20
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)


        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'orig_chg_off_amt': 5
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'orig_chg_off_amt': 10
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'orig_chg_off_amt':15
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'orig_chg_off_amt':20
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=66,
        # 45: NO-previous_values__orig_chg_off_amt == orig_chg_off_amt

        self.assert_evaluator_correct(self.event, 'PROG-ChargeOff-1', self.expected)

    def test_eval_prog_date_closed_1(self):
    # Hits when both condition met:
    # 1. previous_values__date_closed != date_closed
    # 2. port_type == 'I', 'M'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'date_closed':date(2019, 1, 31)
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'date_closed': date(2019, 12, 31)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'date_closed': date(2019, 3, 31)
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'date_closed': date(2019, 5, 31)
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'date_closed': date(2019, 12, 31), 'port_type': 'I'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'date_closed': date(2019, 1, 31), 'port_type': 'M'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'date_closed': date(2019, 3, 31), 'port_type': 'I'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'date_closed': date(2019, 7, 31), 'port_type': 'A'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__date_closed == date_closed
        # 45: NO-port_type='A'

        self.assert_evaluator_correct(self.event, 'PROG-DateClosed-1', self.expected)

    def test_eval_prog_date_open_1(self):
    # Hits when condition met:
    # 1. previous_values__date_open != date_open

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'date_open':date(2019, 1, 31)
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'date_open': date(2019, 12, 31)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'date_open': date(2019, 3, 31)
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'date_open': date(2019, 12, 31)
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'date_open': date(2019, 1, 31)
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'date_open': date(2019, 3, 31)
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__date_open == date_open

        self.assert_evaluator_correct(self.event, 'PROG-DateOpen-1', self.expected)

    def test_eval_prog_dofd_1(self):
    # Hits when all conditions met:
    # 1. previous_values__acct_stat == '61', '62', '63', '64', '65', '71',
    #                 '78', '80' '82', '83', '84', '88', '89', '94', '95',
    #                 '96', '93', '97'
    # 2. acct_stat == '61', '62', '63', '64', '65', '71', '78', '80','82',
    #                 '83', '84', '88', '89', '94', '95', '96', '93', '97'
    # 3. previous_values__dofd != dofd

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

    def test_eval_prog_dofd_2(self):
    # Hits when all conditions met:
    # 1. previous_values__acct_stat == '13'
    # 2. previous_values__pmt != '0'
    # 3. acct_stat == '13'
    # 4. previous_values__dofd != dofd

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': None
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'acct_stat':'11', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 37, 'activity_date': prev_acct_date, 'cons_acct_num': '0037',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 38, 'activity_date': prev_acct_date, 'cons_acct_num': '0038',
                'acct_stat':'13', 'pmt_rating': 0, 'dofd': date(2019, 11, 1)
            }, {
                'id': 39, 'activity_date': prev_acct_date, 'cons_acct_num': '0039',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 11, 1)
            }, {
                'id': 40, 'activity_date': prev_acct_date, 'cons_acct_num': '0040',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': None
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 12, 1)
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'pmt_rating': 0, 'dofd': date(2019, 12, 1)
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 12, 1)
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': None
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': date(2019, 12, 1)
            }, {
                'id': 47, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'acct_stat':'11', 'pmt_rating': 1, 'dofd': date(2019, 12, 1)
            }, {
                'id': 48, 'activity_date': acct_date, 'cons_acct_num': '0038',
                'acct_stat':'13', 'pmt_rating': 0, 'dofd': date(2019, 12, 1)
            }, {
                'id': 49, 'activity_date': acct_date, 'cons_acct_num': '0039',
                'acct_stat':'13', 'pmt_rating': 0, 'dofd': date(2019, 11, 1)
            }, {
                'id': 50, 'activity_date': acct_date, 'cons_acct_num': '0040',
                'acct_stat':'13', 'pmt_rating': 1, 'dofd': None
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: HIT, 45:HIT
        # 46: NO-previous_values__acct-stat=11
        # 47: NO-acct-stat=11
        # 48: NO-previous_values__pmt-rating=0
        # 49: NO-previous_values__dofd == dofd
        # 50: NO-previous_values__dofd == dofd

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'},
            {'id': 43, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033'},
            {'id': 44, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034'},
            {'id': 45, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0035'}]

        self.assert_evaluator_correct(self.event, 'PROG-DOFD-2', expected)

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

    def test_eval_prog_ecoa_1(self):
    # Hits when all conditions met:
    # 1. previous_values__account_holder__ecoa == 'Z',
    # 2. previous_values__account_holder__first_name == account_holder__first_name
    # 3. previous_values__account_holder__surname == account_holder__surname
    # 4. account_holder__ecoa != 'Z'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'ecoa':'A', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 37, 'activity_date': prev_acct_date, 'cons_acct_num': '0037',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'ecoa':'A', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'ecoa':'B', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'ecoa':'A', 'first_name': 'FIRST', 'surname': 'LAST'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'ecoa':'C', 'first_name': 'FIST', 'surname': 'LAST'
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'ecoa':'D', 'first_name': 'FIRST', 'surname': 'LIST'
            }, {
                'id': 47, 'activity_date': acct_date, 'cons_acct_num': '0037',
                'ecoa':'Z', 'first_name': 'FIRST', 'surname': 'LAST'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__account_holder__ecoa == 'A',
        # 45: NO-previous_values__account_holder__first_name != account_holder__first_name
        # 46: previous_values__account_holder__surname != account_holder__surname
        # 47: account_holder__ecoa == 'Z'

        self.assert_evaluator_correct(self.event, 'PROG-ECOA-1', self.expected)

    def test_eval_prog_portfolio_1(self):
    # Hits when condition met:
    # 1. previous_values__port_type != port_type

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'port_type': 'C'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'port_type': 'M'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'port_type': 'I'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'port_type': 'A'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'port_type': 'B'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'port_type': 'I'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__port_type == port_type

        self.assert_evaluator_correct(self.event, 'PROG-Portfolio-1', self.expected)

    def test_eval_prog_rating_1(self):
    # Hits when all conditions met:
    # 1. port_type == 'I', 'M'
    # 2. previous_values__acct_stat == '05', '13',' 62', '65', '88', '89', '94', '95'
    # 3. pmt_rating != previous_values__pmt_rating
    # 4. acct_stat == previous_values__acct_stat

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'port_type': 'I', 'pmt_rating':'0'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'13', 'port_type': 'M', 'pmt_rating':'5'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'61', 'port_type': 'I', 'pmt_rating':'10'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'port_type': 'M', 'pmt_rating':'15'
            }, {
                'id': 36, 'activity_date': prev_acct_date, 'cons_acct_num': '0036',
                'acct_stat':'65', 'port_type': 'I', 'pmt_rating':'20'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'05', 'port_type': 'I', 'pmt_rating':'5'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'12', 'port_type': 'M', 'pmt_rating':'10'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'61', 'port_type': 'I', 'pmt_rating':'15'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'62', 'port_type': 'A', 'pmt_rating':'20'
            }, {
                'id': 46, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'65', 'port_type': 'M', 'pmt_rating':'20'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: NO-acct_stat != previous_values__acct_stat,
        # 44: NO-previous_values__acct_stat=61, 45: NO-port_type='A',
        # 46: NO- pmt_rating == previous_values__pmt_rating

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-Rating-1', expected)

    def test_eval_prog_status_1(self):
    # Hits when the following one conditions are met...
    #   a. previous_values__acct_stat == '71' & acct_stat == '80', '82', '83', '84'
    #   b. previous_values__acct_stat == '78' & acct_stat == '82', '83', '84'
    #   c. previous_values__acct_stat == '80' & acct_stat == '83', '84'
    #   d. previous_values__acct_stat == '82' & acct_stat == '84'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'71'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'78'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'79'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'80'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'80'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'84'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'83'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'82'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=79,
        # 45: NO-acct_stat=82

        self.assert_evaluator_correct(self.event, 'PROG-Status-1', self.expected)

    def test_eval_prog_status_2(self):
    # Hits when both conditions met:
    # 1. previous_values__acct_stat == '89', '94'
    # 2. acct_stat == '97'

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'89'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'97'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'97'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'77'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: NO-previous_values__acct_stat=71,
        # 44: NO-acct_stat=77

        expected = [
            {'id': 42, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}]
        self.assert_evaluator_correct(self.event, 'PROG-Status-2', expected)

    def test_eval_prog_status_3(self):
    # Hits when both conditions met:
    # 1. previous_values__acct_stat == '13', '61', '62', '63', '64', '65'
    # 2. acct_stat != previous_values__acct_stat

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_stat':'61'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_stat':'71'
            }, {
                'id': 35, 'activity_date': prev_acct_date, 'cons_acct_num': '0035',
                'acct_stat':'64'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'97'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'62'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'61'
            }, {
                'id': 45, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'64'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_stat=71,
        # 45: NO-acct_stat == previous_values__acct_stat

        self.assert_evaluator_correct(self.event, 'PROG-Status-3', self.expected)

    def test_eval_prog_type_1(self):
    # Hits when condition met:
    # 1. previous_values__acct_type != acct_type

        # Create previous Account Activities data
        prev_acct_date=date(2019, 11, 30)
        prev_activities = [
            {
                'id': 32, 'activity_date': prev_acct_date, 'cons_acct_num': '0032',
                'acct_type': '00'
            }, {
                'id': 33, 'activity_date': prev_acct_date, 'cons_acct_num': '0033',
                'acct_type': '3A'
            }, {
                'id': 34, 'activity_date': prev_acct_date, 'cons_acct_num': '0034',
                'acct_type': '7A'
            }]
        for r in prev_activities:
            acct_record(self.prev_data_file, r)

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 42, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_type': '0A'
            }, {
                'id': 43, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_type': '6A'
            }, {
                'id': 44, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_type': '7A'
            }]
        for r in activities:
            acct_record(self.data_file, r)
        associate_previous_records(self.event)
        # 42: HIT, 43: HIT, 44: NO-previous_values__acct_type == acct_type

        self.assert_evaluator_correct(self.event, 'PROG-Type-1', self.expected)
