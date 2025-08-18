from datetime import date
from django.test import TestCase

from evaluate_m2.tests.evaluator_test_helper import (
    EvaluatorTestHelper,
    acct_record,
)
from parse_m2.models import Metro2Event, M2DataFile


class PortfolioEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        self.event = Metro2Event.objects.create(name="Test Event")
        self.m2df = M2DataFile.objects.create(event=self.event)
        return super().setUp()

    def test_portfolio_type_1_eval(self):
        activity_date = date(2025, 7, 31)
        records = [
            {'id': 51, 'cons_acct_num': '00251', 'activity_date': activity_date,
             'port_type': 'C', 'acct_type': '14'},  # Hit
            {'id': 52, 'cons_acct_num': '00252', 'activity_date': activity_date,
             'port_type': 'C', 'acct_type': '9E'},  # Hit
            {'id': 53, 'cons_acct_num': '00253', 'activity_date': activity_date,
             'port_type': 'C', 'acct_type': '15'},  # Miss - acct_type
            {'id': 54, 'cons_acct_num': '00254', 'activity_date': activity_date,
             'port_type': 'C', 'acct_type': '7A'},  # Miss - acct_type
            {'id': 55, 'cons_acct_num': '00255', 'activity_date': activity_date,
             'port_type': 'D', 'acct_type': '14'},  # Miss - port_type
            {'id': 56, 'cons_acct_num': '00256', 'activity_date': activity_date,
             'port_type': 'B', 'acct_type': '9E'},  # Miss - port_type
        ]
        for vals in records:
            acct_record(self.m2df, vals)

        expected_results = [
            {'id': 51, 'cons_acct_num': '00251', 'activity_date': activity_date},
            {'id': 52, 'cons_acct_num': '00252', 'activity_date': activity_date},
        ]
        self.assert_evaluator_correct(self.event, 'Portfolio-Type-1', expected_results)
