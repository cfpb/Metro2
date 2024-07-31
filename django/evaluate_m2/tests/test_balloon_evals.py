from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
    k4_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class BalloonEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    def test_eval_account_change_number_4(self):
    # Hits when all conditions are met:
    # 1. current_bal < K4.balloon_pmt_amt

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'current_bal':0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'current_bal':10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'current_bal':20
            }]
        for item in activities:
            acct_record(self.data_file, item)

        k4_activities = [
            {'id': 32, 'balloon_pmt_amt': 5},
            {'id': 33, 'balloon_pmt_amt': 5},
            {'id': 34, 'balloon_pmt_amt': 5}
        ]
        for item in k4_activities:
            k4_record(item)
        # 32: HIT, 33: NO-k4__balloon_pmt_amt < current_bal
        # 34: NO-k4__balloon_pmt_amt < current_bal

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'
        }]

        self.assert_evaluator_correct(
            self.event, 'Balloon-Balance-1', expected)

    def test_eval_account_change_number_4_missing_k4(self):
    # Hits when all conditions are met:
    # 1. current_bal < K4.balloon_pmt_amt

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'current_bal':0
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'current_bal':10
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'current_bal':20
            }]
        for item in activities:
            acct_record(self.data_file, item)

        k4_activities = [
            {'id': 32, 'balloon_pmt_amt': 5},
            {'id': 34, 'balloon_pmt_amt': 5},
        ]
        for item in k4_activities:
            k4_record(item)
        # 32: HIT, 33: NO-missing K4 segment,
        # 34: NO-k4__balloon_pmt_amt < current_bal

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'current_bal':0, 'k4__balloon_pmt_amt': 5
        }]
        self.assert_evaluator_correct(
            self.event, 'Balloon-Balance-1', expected)