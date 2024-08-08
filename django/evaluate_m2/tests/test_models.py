from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from parse_m2.models import Metro2Event


class EvaluateModelsTestCase(TestCase):
    def test_eval_res_create_csv_header(self):
        field_values_json = {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
        }
        eval_res = EvaluatorResult(
            result_summary = EvaluatorResultSummary(),
            field_values = field_values_json,
        )
        expected = [ 'event_name', 'field1', 'field2', 'field3' ]

        self.assertEqual(eval_res.create_csv_header(), expected)

    def test_eval_res_create_csv_row_data(self):
        eval_rs1 = EvaluatorResultSummary(
            event = Metro2Event(name = 'test'),
            evaluator = EvaluatorMetadata(),
            hits = 1
        )
        field_values_json = {
            'field1': 'value1',
            'field2': 'value2',
            'field3': 'value3',
        }

        eval_res = EvaluatorResult(
            result_summary = eval_rs1,
            field_values = field_values_json,
        )
        expected = [ 'test', 'value1', 'value2', 'value3' ]

        self.assertEqual(eval_res.create_csv_row_data(), expected)

    def test_result_summary_fields(self):
        my_evaluator = EvaluatorMetadata(
            id="Sample-Eval-1",
            fields_used=["one", "two", "three"],
            fields_display=["four", "five"]
        )

        field_list = my_evaluator.result_summary_fields()
        expected = ['id', 'activity_date', 'cons_acct_num', 'one', 'two', 'three', 'four', 'five']
        self.assertEqual(field_list, expected)