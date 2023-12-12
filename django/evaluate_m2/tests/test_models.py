from django.test import TestCase

from evaluate_m2.models import EvaluatorMetaData
from evaluate_m2.tests.evaluator_test_helper import EvaluatorTestHelper


class Cat7_EvalsTestCase(TestCase, EvaluatorTestHelper):
    def setUp(self):
        self.expected = 'test'

    def test_set_evaluator_properties_sets_func(self):
        evl = EvaluatorMetaData(name="Test")
        evl.set_evaluator_properties(func="test")

        self.assertEqual(self.expected, evl.func)
        self.assertEqual(None, evl.longitudinal_func)

    def test_set_evaluator_properties_sets_longitudinal_func(self):
        expected = 'test'
        evl = EvaluatorMetaData(name="Test")
        evl.set_evaluator_properties(longitudinal_func="test")

        self.assertEqual(None, evl.func)
        self.assertEqual(self.expected, evl.longitudinal_func)

    def test_exec_custom_func_returns_result(self):
        func = [{'id':1, 'name':'Test_1'}, {'id':2, 'name':'Test_2'}]
        evl = EvaluatorMetaData(name="Test")
        evl.set_evaluator_properties(func=func)

        result = evl.exec_custom_func()

        self.assertEqual(func, result)
