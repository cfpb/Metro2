from unittest import TestCase
from unittest.mock import patch

from metro2.tests.fixtures import Connect, Evaluator, evaluators_test
from metro2.evaluator import evaluators as curr_evals

curr_evals = evaluators_test

from metro2.evaluate import evaluator


class EvaluateTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        evaluator.evaluators["criteria"] = {}
        evaluator.evaluators["criteria"]["test"] = "success"
        cls.test_overwrite = "test"
        cls.test_overwrite_data = "fail"
        cls.test_success = "success"
        cls.test_new = "test2"
        cls.criteria = "criteria"

    # make sure load json fails with invalid file name
    def testLoadJSONFailsWithInvalidFilename(self):
        with self.assertRaises(SystemExit) as cm:
            evaluator.load_json("fail.json")

        self.assertEqual(cm.exception.code, 1)

    # make sure write json doesn't create new directories
    def testWriteJSONFailsWithInvalidDirectory(self):
        with self.assertRaises(SystemExit) as cm:
            evaluator.write_json("metro2/fail/results.json", {})

        self.assertEqual(cm.exception.code, 1)

    @patch('metro2.evaluate.Evaluate.load_json', return_value=None)
    @patch('metro2.evaluate.Evaluate.write_json', return_value=None)
    def testCustomEvaluator(self, *_):
        evaluator.add_custom_evaluator("test.json", self.test_overwrite, self.test_overwrite_data)
        # test that data is not overwritten with duplicate names
        self.assertEqual(evaluator.evaluators[self.criteria][self.test_overwrite], self.test_success)
        evaluator.add_custom_evaluator("test.json", self.test_new, self.test_success)
        # test that new evaluator was created
        self.assertEqual(evaluator.evaluators[self.criteria][self.test_new], {self.test_success})

    # uses fixtures to test evaluator code
    @patch('metro2.evaluator.Evaluator', Evaluator("1A", "success", "success"))
    @patch('sqlalchemy.engine.Engine.connect', return_value=Connect())
    @patch('metro2.tables.connect', return_value=None)
    @patch('metro2.evaluate.Evaluate.load_json', return_value=None)
    @patch('metro2.evaluate.Evaluate.write_json', return_value=None)
    def testRunEvaluators(self, *_):
        evaluator.run_evaluators("test.json")
        print(evaluator.results)
        self.assertEqual(evaluator.results['1A']['description'], 'success')
        self.assertEqual(evaluator.results['1A']['data'], {'a': {'date': 'b', 'fields': ['c', 'd']}})
        self.assertEqual(evaluator.results['1A']['hits'], 1)