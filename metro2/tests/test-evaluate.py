from unittest import TestCase
from unittest.mock import patch

from metro2.evaluate import evaluator
from metro2.tests.fixtures import Connect

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
        self.assertRaises(
            FileNotFoundError,
            evaluator.load_json,
            "fail.xlsx"
        )

    # make sure write json doesn't create new directories
    def testWriteJSONFailsWithInvalidDirectory(self):
        self.assertRaises(
            FileNotFoundError,
            evaluator.write_json,
            "metro2/fail/results.json", {}
        )

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
    # TODO update this to reflect updated evaluating
    # @patch('psycopg2.connect', return_value=Connect())
    # @patch('metro2.evaluate.Evaluate.load_json', return_value=None)
    # @patch('metro2.evaluate.Evaluate.write_json', return_value=None)
    # def testRunEvaluators(self, *_):
    #     evaluator.evaluators["test"] = {
    #         "globals": {
    #             "exam_number": [9999],
    #             "industry_type": ['']
    #         },
    #         "query": "test"
    #     }
    #     evaluator.run_evaluators("test.json")
    #     self.assertEqual(evaluator.results["test"]["hits"], "1")