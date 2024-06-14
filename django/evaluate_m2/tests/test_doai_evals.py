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
        # Create the Account Holders
        self.create_bulk_account_holders(self.data_file, ('Z','Y','X','W','V'))

    ############################
    # Tests for the category addl dofd evaluators

    def test_eval_addl_dofd_4(self):
    # Hits condition is met:
    # 1. doai > (dofd + 7 years)

        # Create the Account Activities data
        activities = {
            'id':(32,33,34,35),
            'cons_acct_num':('0032','0033','0034','0035'),
            'account_holder':('Z','Y','X','W'),
            'dofd':(
                date(2015, 1, 1), date(2015, 12, 31),
                date(2020, 1, 1), date(2020, 1, 1)),
            'doai':(
                date(2023, 1, 1), date(2023, 1, 1),
                date(2023, 1, 1), date(2026, 1, 1))
        }
        # 1: HIT, 2: HIT, 3: NO-3 years, 4: NO-6 years

        self.create_bulk_activities(self.data_file, activities, 4)

        # fields=['database record id', 'activity date', 'consumer account number',
        # 'date of first delinquency', 'date of account information' ],
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'dofd': date(2015, 1, 1),
            'doai': date(2023, 1, 1)
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'dofd': date(2015, 12, 31),
            'doai': date(2023, 1, 1)
        }]
        self.assert_evaluator_correct(self.event, 'DOAI-DOFD-1', expected)

    def test_eval_doai_payment_amount_1(self):
    # Hits condition is met:
    # 1. doai == None
    # 2. actual_pmt_amt > 0

        # Create the Account Activities data
        acct_date=date(2019, 12, 31)
        activities = [
            {
                'id': 32, 'activity_date': acct_date, 'cons_acct_num': '0032',
                'actual_pmt_amt': 1, 'doai': None
            }, {
                'id': 33, 'activity_date': acct_date, 'cons_acct_num': '0033',
                'actual_pmt_amt': 5, 'doai':None
            }, {
                'id': 34, 'activity_date': acct_date, 'cons_acct_num': '0034',
                'actual_pmt_amt': 0, 'doai': None
            }, {
                'id': 35, 'activity_date': acct_date, 'cons_acct_num': '0035',
                'actual_pmt_amt': 10, 'doai':date(2020, 1, 1)
            }]
        for item in activities:
            acct_record(self.data_file, item)
        # 1: HIT, 2: HIT, 3: NO-actual_pmt_amt == 0, 4: NO-doai != None

        # Create the segment data
        expected = [{
            'id': 32, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0032', 'actual_pmt_amt': 1,
            'doai': None
        }, {
            'id': 33, 'activity_date': date(2019, 12, 31),
            'cons_acct_num': '0033', 'actual_pmt_amt': 5,
            'doai': None
        }]
        self.assert_evaluator_correct(self.event, 'DOAI-PaymentAmount-1', expected)
