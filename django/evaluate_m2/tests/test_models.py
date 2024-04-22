from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata, EvaluatorResult, EvaluatorResultSummary
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import Metro2Event


class EvaluateModelsTestCase(TestCase, EvaluatorTestHelper):
    def test_eval_create_from_dict(self):
        input_json = {
            'id': 'Status-DOFD-1',
            'description': 'Account status indicates a delinquent, or paid and previously delinquent, account but there is no date of first delinquency.',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_reference': '41',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        }
        eval = EvaluatorMetadata.create_from_dict(input_json)
        # check that the evaluator was saved in the database
        self.assertIsNotNone(eval.id)
        # check that the properties are correct
        self.assertEqual(eval.id, input_json['id'])
        self.assertEqual(eval.fields_used, ["account status", "date of first delinquency"])

    def test_eval_update_from_dict(self):
        eval1 = EvaluatorMetadata(
            id = "Betsy Test 3",
            description = "Another test evaluator",
            fields_used = ["credit limit", "date closed"],
            crrg_reference = "444",
        )
        input_json = {
            'id': 'Betsy Test 3',
            'description': 'Account status indicates a delinquent, or paid and previously delinquent, account but there is no date of first delinquency.',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'crrg_reference': '41',
            'potential_harm': '',
            'rationale': '',
            'alternate_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
        }

        result = eval1.update_from_dict(input_json)
        self.assertEqual(result.crrg_reference, "41")


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
