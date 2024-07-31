from datetime import date
from django.test import TestCase
from evaluate_m2.evaluate_utils import get_activity_date_range
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import Metro2Event, M2DataFile


class EvaluatorUtilsTestCase(TestCase):
    def test_get_activity_date_range(self):
        # Create test records
        event = Metro2Event.objects.create(name = "test")
        file = M2DataFile.objects.create(event=event, file_name="test")
        acct_record(file, {"id":1, "activity_date": date(2010, 11, 5)})
        acct_record(file, {"id":2, "activity_date": date(2010, 12, 5)})
        acct_record(file, {"id":3, "activity_date": date(2011, 1, 5)})
        acct_record(file, {"id":4, "activity_date": date(2011, 2, 5)})
        record_set = event.get_all_account_activity()

        expected = {
            "earliest": date(2010, 11, 5),
            "latest": date(2011, 2, 5),
        }
        output = get_activity_date_range(record_set)
        self.assertEqual(output, expected)

    def test_get_activity_date_range_when_no_data(self):
        event = Metro2Event.objects.create(name = "test1")
        record_set = event.get_all_account_activity() # should be empty
        expected = {
            "earliest": None,
            "latest": None,
        }
        output = get_activity_date_range(record_set)
        self.assertEqual(output, expected)
