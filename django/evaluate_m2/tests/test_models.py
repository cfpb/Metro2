from django.test import TestCase

from evaluate_m2.models import EvaluatorMetaData
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper
from parse_m2.models import M2DataFile, Metro2Event


class Cat7_EvalsTestCase(TestCase, EvaluatorTestHelper):


    ############################
    # Tests for the models

    def test_set_func_sets_func(self):
        evl = EvaluatorMetaData(name="Test")
        evl.set_func(func=self.set_mock_function)

        self.assertEqual(self.set_mock_function, evl.func)

    def set_mock_function(self):
        return 'test'
