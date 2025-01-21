import io
import datetime
from django.test import TestCase

from evaluate_m2.upload_utils import (
    generate_full_csv, generate_json_sample,
    full_s3_url, s3_bucket_key, s3_filename
)
from evaluate_m2.models import (
    EvaluatorMetadata,
    EvaluatorResult,
    EvaluatorResultSummary,
)
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import (
    AccountActivity,
    Metro2Event,
    M2DataFile,
)

class UploadUtilsTestCase(TestCase):
    def setUp(self):
        event = Metro2Event.objects.create(name="MyEVENT")
        eval = EvaluatorMetadata.objects.create(id="my-eval-3", fields_used=["amt_past_due", "account_holder__ecoa"], fields_display=["doai"])
        f = M2DataFile.objects.create(event=event)
        r1 = acct_record(f, {"id": 1, "cons_acct_num": "41", "ecoa": "AB"})
        r2 = acct_record(f, {"id": 2, "cons_acct_num": "42", "ecoa": "AC"})
        r3 = acct_record(f, {"id": 3, "cons_acct_num": "43", "ecoa": ""})
        r4 = acct_record(f, {"id": 4, "cons_acct_num": "44", "ecoa": "AE"})
        self.ers = EvaluatorResultSummary.objects.create(event=event, evaluator=eval, hits=4)
        EvaluatorResult.objects.create(date=r1.activity_date, result_summary=self.ers, source_record=r1)
        EvaluatorResult.objects.create(date=r2.activity_date, result_summary=self.ers, source_record=r2)
        EvaluatorResult.objects.create(date=r3.activity_date, result_summary=self.ers, source_record=r3)
        EvaluatorResult.objects.create(date=r4.activity_date, result_summary=self.ers, source_record=r4)
        return super().setUp()

    def test_generate_results_csv(self):
        expected = '\r\n'.join([
            "event_name,id,activity_date,cons_acct_num,amt_past_due,account_holder__ecoa,doai",
            "MyEVENT,1,2022-05-30,41,0,AB,2022-05-01",
            "MyEVENT,2,2022-05-30,42,0,AC,2022-05-01",
            "MyEVENT,3,2022-05-30,43,0,,2022-05-01",
            "MyEVENT,4,2022-05-30,44,0,AE,2022-05-01",
            ""
        ])

        with io.StringIO() as f:
            generate_full_csv(self.ers, f)
            f.seek(0)
            result = f.read()
        self.assertEqual(expected, result)

    def test_generate_sample_json(self):
        # When the eval result summary specifies the sample ID list,
        # the response includes only the records in that list
        self.ers.sample_ids=[2, 4]
        expected = {
            'hits': [
                {'id': 2, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '42', 'amt_past_due': 0,
                 'account_holder__ecoa': "AC",
                 'doai': datetime.date(2022, 5, 1)},
                {'id': 4, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '44', 'amt_past_due': 0,
                 'account_holder__ecoa': "AE",
                 'doai': datetime.date(2022, 5, 1)}
            ]
        }
        result = generate_json_sample(self.ers, AccountActivity.objects)
        self.assertEqual(expected, result)

    def test_generate_sample_json_sample_ids_missing(self):
        # When the eval result summary doesn't specify a sample ID list,
        # the response includes all results (up to a max of M2_RESULT_SAMPLE_SIZE)
        self.ers.sample_ids=[]
        expected = {
            'hits': [
                {'id': 1, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '', 'amt_past_due': 0,
                 'account_holder__ecoa': "AB",
                 'doai': datetime.date(2022, 5, 1)},
                {'id': 2, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '', 'amt_past_due': 0,
                 'account_holder__ecoa': "AC",
                 'doai': datetime.date(2022, 5, 1)},
                {'id': 3, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '', 'amt_past_due': 0,
                 'account_holder__ecoa': "",
                 'doai': datetime.date(2022, 5, 1)},
                {'id': 4, 'activity_date': datetime.date(2022, 5, 30),
                 'cons_acct_num': '', 'amt_past_due': 0,
                 'account_holder__ecoa': "AE",
                 'doai': datetime.date(2022, 5, 1)}
            ]
        }
        result = generate_json_sample(self.ers, AccountActivity.objects)
        self.assertEqual(expected, result)

    def test_get_url(self):
        with self.settings(S3_BUCKET_NAME = 'sample-bucket'):
            result = full_s3_url(event_id=5, evaluator_id='sample-eval-3', file_ext='json')
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
