from django.test import TestCase

from evaluate_m2.models import EvaluatorMetadata
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper


class EvaluateModelsTestCase(TestCase, EvaluatorTestHelper):
    def test_set_func_sets_func(self):
        evl = EvaluatorMetadata(name="Test")
        evl.set_func(func=self.set_mock_function)

        self.assertEqual(self.set_mock_function, evl.func)

    def set_mock_function(self):
        return 'test'
