import unittest
import evaluate

from evaluate import evaluator
from fixtures import Engine, ExpectedException, Evaluator
from unittest.mock import patch

class TestEvaluate(unittest.TestCase):
    def test_run_evaluators_no_evals(self):
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators()
        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        expected = list()
        self.assertListEqual(expected, evaluator.statements)
        self.assertListEqual(expected, evaluator.metadata_statements)

    @patch(evaluate.create_engine)
    def test_run_evaluators_engine_exception(self, mock_create_engine):
        # mocks calls that happen within the run_evaluators function to 
        # trigger an exception and assert that dispose was called by 
        # having it return ExpectedException
        mock_create_engine.return_value = Engine(connect_return=Exception(),
            dispose_return=ExpectedException()
        )
        evaluator.evaluators = []
        self.assertRaises(ExpectedException, evaluator.run_evaluators)

    @patch(evaluate.create_engine)
    def test_run_evaluators_set_globals_called(self, mock_create_engine):
        # mocks calls that happen within the run_evaluators function to
        # trigger an exception and assert that set_globals was called
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException()
        )
        evaluator.evaluators = [Evaluator(set_globals_return=Exception())]
        self.assertRaises(ExpectedException, evaluator.run_evaluators)

    @partch(evaluate.create_engine)
    def test_run_evaluators_produces_results(self, mock_create_engine):
        # should correctly insert one statement and one metadata statement
        mock_create_engine.return_value = Engine()
        results = [1, 2, 3, [1, 2]]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["Field 1", "Field 2"]
        )]
        self.assertEqual(1, len(evaluator.statements))
        self.assertEqual(1, len(evaluator.metadata_statements))

    @partch(evaluate.create_engine)
    def test_run_evaluators_produces_results(self, mock_create_engine):
        # should raise an exception when there are less than 3 fields in
        # results
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException()
        )
        results = [1, 2]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["Field 1", "Field 2"]
        )]
        self.assertRaises(ExpectedException, evaluator.run_evaluators)
