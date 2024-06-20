from django.test import TestCase

from datetime import date
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper, acct_record
from parse_m2.models import Metro2Event, M2DataFile

class DateClosedEvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        # Create the parent records for the AccountActivity data
        self.event = Metro2Event(name='test_exam')
        self.event.save()
        self.data_file = M2DataFile(event=self.event, file_name='file.txt')
        self.data_file.save()
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V'))

    ############################
    # Tests for the category addl dofd evaluators

    def test_eval_dtcl_dolp_1(self):
    # Hits when all conditions are met:
    # 1. port_type  == 'I', 'M'
    # 2. acct_stat == '13', '61', '62', '63', '64', '65'
    # 3. date_closed != dolp

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'acct_stat':'13', 'port_type': 'I', 'date_closed': None,
                'dolp':date(2020, 1, 1)
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'acct_stat':'61', 'port_type': 'M', 'date_closed':date(2020, 1, 1),
                'dolp':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'acct_stat':'62', 'port_type': 'C', 'date_closed': None,
                'dolp':date(2020, 1, 1)
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'acct_stat':'01', 'port_type': 'I', 'date_closed':date(2020, 1, 1),
                'dolp':None
            }, {
                'id': 36, 'activity_date': acct_date, 'cons_acct_num': '0036',
                'acct_stat':'63', 'port_type': 'M', 'date_closed':date(2020, 1, 1),
                'dolp':date(2020, 1, 1)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 32: HIT, 33: HIT, 34: NO-port_type=C,
        # 35: NO-acct_stat=01, 36: No-date_closed=dolp

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'port_type':'I', 'acct_stat':'13',
            'date_closed': None,'dolp': date(2020, 1, 1)
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'port_type':'M', 'acct_stat':'61',
            'date_closed': date(2020, 1, 1),'dolp': None
        }]
        self.assert_evaluator_correct(
            self.event, 'DTCL-DOLP-1', expected)
