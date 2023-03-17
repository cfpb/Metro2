from unittest import TestCase
from unittest.mock import patch

from metro2.evaluate import evaluator


class TestEvaluateTestCase(TestCase):
    @classmethod
    def set_up_class(cls):
        evaluator.evaluators["criteria"] = {}
        evaluator.evaluators["criteria"]["test"] = "success"
        cls.test_overwrite = "test"
        cls.test_overwrite_data = "fail"
        cls.test_success = "success"
        cls.test_new = "test2"
        cls.criteria = "criteria"

    # make sure load json fails with invalid file name
    def test_load_JSON_fails_with_invalid_filename(self):
        with self.assertRaises(SystemExit) as cm:
            evaluator.load_json("fail.json")

        self.assertEqual(cm.exception.code, 1)

    # make sure write json doesn't create new directories
    def test_write_JSON_fails_with_invalid_directory(self):
        with self.assertRaises(SystemExit) as cm:
            evaluator.write_json("metro2/fail/results.json", {})

        self.assertEqual(cm.exception.code, 1)

    @patch('metro2.evaluate.Evaluate.load_json', return_value=None)
    @patch('metro2.evaluate.Evaluate.write_json', return_value=None)
    def test_custom_evaluator(self, *_):
        evaluator.add_custom_evaluator("test.json", self.test_overwrite, self.test_overwrite_data)
        # test that data is not overwritten with duplicate names
        self.assertEqual(evaluator.evaluators[self.criteria][self.test_overwrite], self.test_success)
        evaluator.add_custom_evaluator("test.json", self.test_new, self.test_success)
        # test that new evaluator was created
        self.assertEqual(evaluator.evaluators[self.criteria][self.test_new], {self.test_success})

    # uses fixtures to test evaluator code
    # TODO: test run_evaluators. Removed for now because the test relied too heavily on mocking.