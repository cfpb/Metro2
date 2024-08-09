from datetime import date
from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import acct_record
from parse_m2.models import M2DataFile, Metro2Event


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

        self.assertEqual(eval_res.create_csv_header(), expected)

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