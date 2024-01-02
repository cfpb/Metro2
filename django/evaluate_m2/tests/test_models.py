from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper


class EvaluateModelsTestCase(TestCase, EvaluatorTestHelper):
    def test_eval_create_from_dict(self):
        input_json = {
            'name': 'ADDL-DOFD-1',
            'description': 'Account status indicates a delinquent, or paid and previously delinquent, account but there is no date of first delinquency.',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'ipl': '',
            'crrg_topics': '',
            'crrg_page': '41',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            'risk_level': 'High'
        }
        eval = EvaluatorMetadata.create_from_dict(input_json)
        # check that the evaluator was saved in the database
        self.assertIsNotNone(eval.id)
        # check that the properties are correct
        self.assertEqual(eval.name, input_json['name'])
        self.assertEqual(eval.fields_used, ["account status", "date of first delinquency"])

    def test_eval_update_from_dict(self):
        eval1 = EvaluatorMetadata(
            name = "Betsy Test 3",
            description = "Another test evaluator",
            fields_used = ["credit limit", "date closed"],
            crrg_page = "444",
            risk_level = "Low"
        )
        input_json = {
            'name': 'Betsy Test 3',
            'description': 'Account status indicates a delinquent, or paid and previously delinquent, account but there is no date of first delinquency.',
            'long_description': '',
            'fields_used': 'account status;date of first delinquency',
            'fields_display': 'amount past due;compliance condition code;current balance;date closed;original charge-off amount;scheduled monthly payment amount;special comment code;terms frequency',
            'ipl': '',
            'crrg_topics': '',
            'crrg_page': '41',
            'pdf_page': '',
            'use_notes': '',
            'alternative_explanation': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua',
            'risk_level': 'High'
        }

        result = eval1.update_from_dict(input_json)
        self.assertEqual(result.crrg_page, "41")
        self.assertEqual(result.risk_level, "High")

    def test_serialize_eval(self):
        eval1 = EvaluatorMetadata(
            name = "Betsy Test 1",
            description = "My test evaluator",
            fields_used = ["credit limit", "date closed"],
            crrg_page = "444",
            risk_level = "Low"
        )

        expected = [
            "Betsy Test 1",             # self.name
            "My test evaluator",        # self.description
            "",                         # self.long_description
            "credit limit;date closed", # self.fields_used
            "",                         # self.fields_display
            "",                         # self.ipl
            "",                         # self.crrg_topics
            "444",                      # self.crrg_page
            "",                         # self.pdf_page
            "",                         # self.use_notes
            "",                         # self.alternative_explanation
            "Low",                      # self.risk_level
        ]
        self.assertEqual(eval1.serialize(), expected)
