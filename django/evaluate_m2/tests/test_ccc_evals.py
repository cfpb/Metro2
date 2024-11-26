from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class CCCEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the previous AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    # Hits when all conditions are met:
    # 1. compl_cond_cd == 'XA'
    # 3. date_closed == None
    def test_eval_ccc_date_closed_1(self):
        # Create previous Account Activities data
        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'11', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'71', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'12', 'compl_cond_cd': 'XA', 'date_closed': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'78', 'compl_cond_cd': 'XB', 'date_closed': None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'80', 'compl_cond_cd': 'XA', 'date_closed': date(2020, 1, 1)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: HIT,
        # 35: NO-compl_cond_cd=XB, 36: No-date_closed=date(2020, 1, 1)

        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032',
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0033',
        }, {
            'id': 34, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0034',
        }]
        self.assert_evaluator_correct(
            self.event, 'CCC-DateClosed-1', expected)
