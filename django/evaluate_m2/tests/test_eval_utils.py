from datetime import date
from django.test import TestCase
from evaluate_m2.evaluate_utils import get_activity_date_range, every_month_in_range
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event, M2DataFile, AccountActivity, AccountHolder


class Cat9_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self) -> None:
        event = Metro2Event(name = "test")
        event.save()
        file = M2DataFile(event=event, file_name="test")
        file.save()
        # previous year record
        a0_date = date(2010, 12,5)
        a0_acct_holder = AccountHolder(data_file=file, activity_date=a0_date)
        a0_acct_holder.save()
        self.a0 = AccountActivity(
            account_holder=a0_acct_holder,activity_date = a0_date, date_open = a0_date, credit_limit=0, hcola=0, smpa=0, actual_pmt_amt=0, current_bal=0, amt_past_due=0, orig_chg_off_amt=0, doai=a0_date
        )
        self.a0.save()
        # first record
        a1_date = date(2011, 1,5)
        a1_acct_holder = AccountHolder(data_file=file, activity_date=a1_date)
        a1_acct_holder.save()
        self.a1 = AccountActivity(
            account_holder=a1_acct_holder,activity_date = a1_date, date_open = a1_date, credit_limit=1, hcola=1, smpa=1, actual_pmt_amt=1, current_bal=1, amt_past_due=1, orig_chg_off_amt=1, doai=a1_date
        )
        self.a1.save()
        # second record
        a2_date = date(2011, 2,5)
        a2_acct_holder = AccountHolder(data_file=file, activity_date=a2_date)
        a2_acct_holder.save()
        self.a2 = AccountActivity(
            account_holder=a2_acct_holder,activity_date = a2_date, date_open = a2_date, credit_limit=2, hcola=2, smpa=2, actual_pmt_amt=2, current_bal=2, amt_past_due=2, orig_chg_off_amt=2, doai=a2_date
        )
        self.a2.save()
        # third record
        a3_date = date(2011, 3,5)
        a3_acct_holder = AccountHolder(data_file=file, activity_date=a3_date)
        a3_acct_holder.save()
        self.a3 = AccountActivity(
            account_holder=a3_acct_holder,activity_date = a3_date, date_open = a3_date, credit_limit=3, hcola=3, smpa=3, actual_pmt_amt=3, current_bal=3, amt_past_due=3, orig_chg_off_amt=3, doai=a3_date
        )
        self.a3.save()

        self.record_set = event.get_all_account_activity()


    def test_get_activity_date_range(self):
        expected = {
            "earliest": self.a0.activity_date,
            "latest": self.a3.activity_date,
        }
        output = get_activity_date_range(self.record_set)
        self.assertEqual(output, expected)

    def test_get_months_in_range(self):
        start_date = date(2021, 11, 25)  # the "day" value is ignored
        end_date = date(2022, 2, 2)
        expected = [
            {"year": 2021, "month": 11},
            {"year": 2021, "month": 12},
            {"year": 2022, "month": 1},
            {"year": 2022, "month": 2},
        ]
        result = every_month_in_range(start_date, end_date)
        self.assertEqual(result, expected)

    def test_get_months_in_longer_range(self):
        start_date = date(2020, 11, 25)  # the "day" value is ignored
        end_date = date(2022, 2, 2)
        expected = [
            {"year": 2020, "month": 11},
            {"year": 2020, "month": 12},
            {"year": 2021, "month": 1},
            {"year": 2021, "month": 2},
            {"year": 2021, "month": 3},
            {"year": 2021, "month": 4},
            {"year": 2021, "month": 5},
            {"year": 2021, "month": 6},
            {"year": 2021, "month": 7},
            {"year": 2021, "month": 8},
            {"year": 2021, "month": 9},
            {"year": 2021, "month": 10},
            {"year": 2021, "month": 11},
            {"year": 2021, "month": 12},
            {"year": 2022, "month": 1},
            {"year": 2022, "month": 2},
        ]
        result = every_month_in_range(start_date, end_date)
        self.assertEqual(result, expected)
