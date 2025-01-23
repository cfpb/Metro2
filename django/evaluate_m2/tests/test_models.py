from datetime import date
from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


class ResultSampleTestCase(TestCase):
    def setUp(self):
        event = Metro2Event.objects.create(name="MyeVent")
        eval = EvaluatorMetadata.objects.create(id="my-eval-3", fields_used=["amt_past_due"], fields_display=["doai"])
        f = M2DataFile.objects.create(event=event)
        r1 = acct_record(f, {"id": 31})
        r2 = acct_record(f, {"id": 32})
        r3 = acct_record(f, {"id": 33})
        r4 = acct_record(f, {"id": 34})
        self.ers = EvaluatorResultSummary.objects.create(event=event, evaluator=eval, hits=4)
        EvaluatorResult.objects.create(date=r1.activity_date, result_summary=self.ers, source_record=r1)
        EvaluatorResult.objects.create(date=r2.activity_date, result_summary=self.ers, source_record=r2)
        EvaluatorResult.objects.create(date=r3.activity_date, result_summary=self.ers, source_record=r3)
        EvaluatorResult.objects.create(date=r4.activity_date, result_summary=self.ers, source_record=r4)

    def test_sample_randomize(self):
        result = self.ers.sample_of_results(sample_size=2)

        # There should be two items in the list
        self.assertEqual(len(result), 2)
        for x in result:
            # each item in the list should match an AccountActivity ID
            self.assertTrue(x in [31, 32, 33, 34])
        # IDs in the list should not be repeated
        self.assertNotEqual(result[0], result[1])

    def test_sample_when_not_randomized(self):
        # sample_size is greater than the number of results, so all should be included
        result = self.ers.sample_of_results(sample_size=5)
        self.assertEqual(sorted(result), [31, 32, 33, 34])


class EvaluateModelsTestCase(TestCase):
    def test_eval_res_create_csv_header(self):
        field_values_json = {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
        }
        eval = EvaluatorMetadata(
            id="event_name",
            fields_used=['field1', 'field2', 'field3'],
            fields_display=[]
        )
        eval_rs1 = EvaluatorResultSummary(
            event = Metro2Event(name = 'test'),
            evaluator = eval,
            hits = 1
        )
        eval_res = EvaluatorResult(
            result_summary = eval_rs1,
            field_values = field_values_json,
        )
        expected = ['event_name', 'id', 'activity_date',
            'cons_acct_num', 'field1', 'field2', 'field3']

        self.assertEqual(eval_rs1.create_csv_header(), expected)

    def test_eval_res_create_csv_row_data(self):
        acct_date=date(2019, 12, 31)
        event = Metro2Event.objects.create(name = 'test')
        data_file = M2DataFile.objects.create(event=event, file_name='file.txt')
        record = acct_record(data_file, {'id': 1, 'cons_acct_num': '001',
                                         'activity_date': acct_date})
        eval_rs1 = EvaluatorResultSummary(
            event = event,
            evaluator = EvaluatorMetadata(),
            hits = 1
        )

        eval_res = EvaluatorResult(
            result_summary = eval_rs1,
            source_record = record
        )
        field_list = ['id', 'cons_acct_num', 'activity_date']
        expected = [ 'test', 1, '001', acct_date ]
        self.assertEqual(eval_res.create_csv_row_data(field_list), expected)

    def test_result_summary_fields(self):
        my_evaluator = EvaluatorMetadata(
            id="Sample-Eval-1",
            fields_used=["one", "two", "three"],
            fields_display=["four", "five"]
        )

        field_list = my_evaluator.result_summary_fields()
        expected = ['id', 'activity_date', 'cons_acct_num', 'one', 'two', 'three', 'four', 'five']
        self.assertEqual(field_list, expected)
