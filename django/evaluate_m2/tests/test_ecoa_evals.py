from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile

class DOAIEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()

    ############################
    # Tests for the category ecoa evaluators

    def test_eval_ecoa_j1j2_1(self):
    # Hits condition is met:
    # 1. ecoa == 'X'
    # 2. ecoa_assoc != 'X'

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'ecoa': 'X', 'ecoa_assoc': ['T', '7']
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
              'ecoa': '1', 'ecoa_assoc': ['T', '7']
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
              'ecoa': 'X', 'ecoa_assoc': ['X', '7']
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: NO-ecoa=1, 34: NO-ecoa_assoc='X'

        expected = [
            {'id': 32, 'activity_date': date(2019, 12, 31), 'cons_acct_num': '0032'}
        ]

        self.assert_evaluator_correct(self.event, 'ECOA-J1J2-1', expected)
