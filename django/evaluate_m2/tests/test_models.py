from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper


class EvaluateModelsTestCase(TestCase, EvaluatorTestHelper):
    mock_function = lambda: "mock output"

    def test_set_func_sets_func(self):
        evl = EvaluatorMetadata(name="Test")
        evl.set_func(func=self.mock_function)

        self.assertEqual(self.mock_function, evl.func)
