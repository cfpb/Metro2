from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
    l1_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class AccountChangeEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the category AccountChange evaluators
    def test_eval_account_change_id_1(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '2', '3'
    # 2. l1__new_id_num == ''

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '2', 'new_id_num':'', 'new_acc_num': '32'},
            {'id': 34, 'change_ind': '1', 'new_id_num':'a', 'new_acc_num': ''},
            {'id': 35, 'change_ind': '3', 'new_id_num':'2', 'new_acc_num': '35'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: NO-missing L1 segment,
        # 34: NO-l1_change_ind=2, 35: NO-l1__new_id_num=2

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__change_ind':'2',
            'l1__new_acc_num':'32', 'l1__new_id_num': ''
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-ID-1', expected)

    def test_eval_account_change_id_2(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '1'
    # 2. l1__new_id_num != ''

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '1', 'new_id_num':'2', 'new_acc_num': '32'},
            {'id': 34, 'change_ind': '2', 'new_id_num':'3', 'new_acc_num': ''},
            {'id': 35, 'change_ind': '1', 'new_id_num':'', 'new_acc_num': '35'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: NO-missing L1 segment,
        # 34: NO-l1_change_ind=2, 35: NO-l1__new_id_num=''

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__change_ind':'1',
            'l1__new_acc_num':'32', 'l1__new_id_num': '2'
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-ID-2', expected)

    def test_eval_account_change_id_3(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '2', '3'
    # 2. l1__new_id_num == id_num

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'id_num': 'a'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'id_num': 'b'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'id_num': 'c'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'id_num': 'd'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '2', 'new_id_num':'A', 'new_acc_num': ''},
            {'id': 34, 'change_ind': '1', 'new_id_num':'c', 'new_acc_num': ''},
            {'id': 35, 'change_ind': '3', 'new_id_num':'e', 'new_acc_num': '35'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: NO-missing L1 segment,
        # 34: NO-l1_change_ind=1, 35: NO-l1__new_id_num='e'

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'id_num':  'a', 'l1__change_ind':'2',
            'l1__new_acc_num':'', 'l1__new_id_num': 'A'
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-ID-3', expected)

    def test_eval_account_change_number_1(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '1', '3'
    # 2. l1__new_acc_num == ''

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '1', 'new_acc_num': ''},
            {'id': 34, 'change_ind': '2', 'new_acc_num': ''},
            {'id': 35, 'change_ind': '3', 'new_acc_num': '0036'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: NO-missing L1 segment,
        # 34: NO-l1_change_ind=2, 35: NO-l1__new_acc_num=0036

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__change_ind':'1',
            'l1__new_acc_num':'', 'l1__new_id_num': ''
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-Number-1', expected)

    def test_eval_account_change_number_2(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '2'
    # 2. l1__new_acc_num != ''

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '2', 'new_acc_num': '32'},
            {'id': 34, 'change_ind': '1', 'new_acc_num': '34'},
            {'id': 35, 'change_ind': '2', 'new_acc_num': ''},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: NO-missing L1 segment,
        # 34: NO-l1_change_ind=1, 35: NO-l1__new_acc_num=''

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__change_ind':'2',
            'l1__new_acc_num':'32', 'l1__new_id_num': ''
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-Number-2', expected)

    def test_eval_account_change_number_3(self):
    # Hits when all conditions are met:
    # 1. l1_change_ind == '1', '3'
    # 2. l1__new_acc_num == cons_acct_num

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': 'O33'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'change_ind': '1', 'new_acc_num': '0032'},
            {'id': 33, 'change_ind': '3', 'new_acc_num': 'o33'},
            {'id': 34, 'change_ind': '2', 'new_acc_num': '0034'},
            {'id': 35, 'change_ind': '2', 'new_acc_num': '35'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: HIT - lowercase/uppercase O,
        # 34: NO-l1__change_ind=2,
        # 35: NO-l1__new_acc_num=35

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__change_ind': '1',
            'l1__new_acc_num':'0032', 'l1__new_id_num': ''
        },
        {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': 'O33', 'l1__change_ind': '3',
            'l1__new_acc_num':'o33', 'l1__new_id_num': ''
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-Number-3', expected)

    def test_eval_account_change_number_4(self):
    # Hits when all conditions are met:
    # 1. cons_acct_num == L1.new_acc_num

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032'
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': 'O33'
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034'
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035'
            }]
        for item in activities:
            acct_record(self.data_file, item)

        l1_activities = [
            {'id': 32, 'new_acc_num': '0032'},
            {'id': 33, 'new_acc_num': 'o33'},
            {'id': 35, 'new_acc_num': '0037'},
        ]
        for item in l1_activities:
            l1_record(item)
        # 32: HIT, 33: HIT - lowercase/uppercase O,
        # 34: NO-missing L1 segment,
        # 35: NO-l1__new_acc_num=0037

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'l1__new_acc_num':'0032'
        },
        {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': 'O33', 'l1__new_acc_num':'o33'
        }]
        self.assert_evaluator_correct(
            self.event, 'AccountChange-Number-4', expected)