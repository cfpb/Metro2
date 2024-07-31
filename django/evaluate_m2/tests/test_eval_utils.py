from datetime import date
from django.test import TestCase
import re
from evaluate_m2.evaluate_utils import get_activity_date_range, create_eval_insert_query
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import Metro2Event, M2DataFile, AccountActivity
from evaluate_m2.models import EvaluatorMetadata, EvaluatorResultSummary


class EvaluatorUtilsTestCase(TestCase):
    def setUp(self) -> None:
        self.event = Metro2Event.objects.create(name = "test")
        eval = EvaluatorMetadata.objects.create(id="Sample-1")
        self.result_summary = EvaluatorResultSummary.objects.create(event=self.event, evaluator=eval, hits=0)

    def test_get_activity_date_range(self):
        # Create test records
        file = M2DataFile.objects.create(event=self.event, file_name="test")
        acct_record(file, {"id":1, "activity_date": date(2010, 11, 5)})
        acct_record(file, {"id":2, "activity_date": date(2010, 12, 5)})
        acct_record(file, {"id":3, "activity_date": date(2011, 1, 5)})
        acct_record(file, {"id":4, "activity_date": date(2011, 2, 5)})
        record_set = self.event.get_all_account_activity()

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

    def test_insert_query_creates_expected_sql(self):
        # A query on the AccountActivity table matches the expected format of an evaluator
        # The exact query doesn't matter, it just needs to follow the evaluator pattern
        account_query = AccountActivity.objects.filter(port_type="A")
        # Get the SQL of the query the same way we do in the evaluator
        acct_query_sql = account_query.query.sql_with_params()[0]

        # Generate the sql for the insert query
        result_sql = create_eval_insert_query(acct_query_sql, self.result_summary)

        # Ensure sql matches expected pattern:
        #    INSERT into evaluate_m2_evaluatorresult [specific fields]
        #    SELECT [specific fields] FROM parse_m2_accountactivity
        regex_check = re.compile('^\s*INSERT INTO evaluate_m2_evaluatorresult\s* \(source_record_id, date, acct_num, result_summary_id\)\s*SELECT\s*parse_m2_accountactivity\.id,\s*parse_m2_accountactivity\.activity_date,\s*parse_m2_accountactivity\.cons_acct_num,\s*\d?\d FROM parse_m2.accountactivity')
        self.assertRegex(result_sql, regex_check)

    def test_insert_query_errors_with_bad_input(self):
        # A query on the M2DataFile table does not match the expected evaluator format.
        wrong_query = M2DataFile.objects.filter(error_message="hello")
        wrong_query_sql = wrong_query.query.sql_with_params()[0]

        # Since the query isn't of the expected type, the method raises a TypeError.
        with self.assertRaises(TypeError):
            create_eval_insert_query(wrong_query_sql, self.result_summary)
