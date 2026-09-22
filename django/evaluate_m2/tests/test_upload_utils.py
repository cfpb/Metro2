import csv
import io

from django.test import TestCase

from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary,
    EvaluatorResultMaterializedView,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record
from evaluate_m2.upload_utils import (
    full_s3_url,
    generate_eval_results_csv,
    s3_bucket_key,
    s3_filename,
)
from parse_m2.models import (
    M2DataFile,
    Metro2Event,
)


class UploadUtilsTestCase(TestCase):
    def setUp(self):
        event = Metro2Event.objects.create(name="MyEVENT")
        self.eval = EvaluatorMetadata.objects.create(
            id="my-eval-3",
            fields_used=["amt_past_due", "ecoa"],
            fields_display=["doai"]
        )
        f = M2DataFile.objects.create(event=event)
        r1 = acct_record(f, {"id": 1, "cons_acct_num": "41", "ecoa": "AB"})
        r2 = acct_record(f, {"id": 2, "cons_acct_num": "42", "ecoa": "AC"})
        r3 = acct_record(f, {"id": 3, "cons_acct_num": "43", "ecoa": ""})
        r4 = acct_record(f, {"id": 4, "cons_acct_num": "44", "ecoa": "AE"})
        self.ers = EvaluatorResultSummary.objects.create(
            event=event,
            evaluator=self.eval,
            hits=4
        )
        EvaluatorResult.objects.create(
            date=r1.activity_date,
            result_summary=self.ers,
            source_record=r1
        )
        EvaluatorResult.objects.create(
            date=r2.activity_date,
            result_summary=self.ers,
            source_record=r2
        )
        EvaluatorResult.objects.create(
            date=r3.activity_date,
            result_summary=self.ers,
            source_record=r3
        )
        EvaluatorResult.objects.create(
            date=r4.activity_date,
            result_summary=self.ers,
            source_record=r4
        )
        EvaluatorResultMaterializedView.create_or_refresh_materialized_view()
        return super().setUp()

    expected_csv_headers = [
        'Activity date',
        'Account number',
        'Portfolio type',
        'Account type',
        'Date opened',
        'Credit limit',
        'HCOLA',
        'ID number',
        'Terms duration',
        'Terms frequency',
        'Scheduled monthly payment amount',
        'Actual payment amount',
        'Account status',
        'Payment rating',
        'Payment history profile (all entries)',
        'Payment history profile',
        'Special comment code',
        'Compliance condition code',
        'Current balance',
        'Amount past due',
        'Original charge-off amount',
        'Date of account information',
        'DOFD',
        'Date closed',
        'Date of last payment',
        'Interest type indicator',
        'ECOA code for account holder',
        'ECOA codes for associated consumers',
        'Consumer information indicator',
        'Consumer information indicator - J1+J2 segments',
        'Purchased-sold indicator (K2)',
        'Purchased-sold name (K2)',
        'Specialized payment indicator (K4)',
        'Deferred payment start date (K4)',
        'Balloon payment due date (K4)',
        'Balloon payment amount (K4)',
        'Account change indicator (L1)',
        'New consumer account number (L1)',
        'New identification number (L1)',
        'Prior activity date',
        'Prior portfolio type',
        'Prior account type',
        'Prior date open',
        'Prior ID number',
        'Prior account status',
        'Prior payment rating',
        'Prior current balance',
        'Prior original charge-off amount',
        'Prior DOFD',
        'Prior date closed',
        'Prior ECOA code for account holder',
        'Prior ECOA codes for associated consumers',
        'Prior bankruptcy - Consumer information indicator for account holder',
        'Prior bankruptcy - Consumer information indicator for associated consumers',
        'Prior account change indicator (L1)',
        'Prior new consumer account number (L1)',
        'Prior new identification number (L1)',
    ]

    def test_generate_results_csv(self):
        qs = EvaluatorResultMaterializedView.objects.all()
        with io.StringIO() as f:
            generate_eval_results_csv(qs, f)
            f.seek(0)
            result = f.read().splitlines()

        self.assertEqual(result[0].split(','), self.expected_csv_headers)
        # CSV output should have 4 results, plus a header row
        self.assertEqual(len(result), 5)
        # Check the content of the CSV output
        csvreader = csv.DictReader(result)
        for row in csvreader:
            self.assertEqual(row['Activity date'], '2022-05-30')
            self.assertIn(
                row['Account number'],
                ['41', '42', '43', '44'])

    def test_get_url(self):
        with self.settings(S3_BUCKET_NAME = 'sample-bucket'):
            result = full_s3_url(
                event_id=5,
                evaluator_id='sample-eval-3',
                file_ext='json'
            )
            expected = "s3://sample-bucket/eval_results/event_5/sample-eval-3.json"
            self.assertEqual(result, expected)

    def test_s3_filename(self):
        result = s3_filename('my-eval-4', 'txt')
        expected = "my-eval-4.txt"
        self.assertEqual(result, expected)

    def test_s3_bucket_key(self):
        result = s3_bucket_key(event_id=11, evaluator_id='prog-eval-9', file_ext='jpg')
        expected = "eval_results/event_11/prog-eval-9.jpg"
        self.assertEqual(result, expected)
