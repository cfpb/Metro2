import unittest

from evaluate import evaluator
from tests.fixtures import Engine, Evaluator, Connection
from unittest.mock import patch

class TestEvaluate(unittest.TestCase):

    ###########################################################################
    # Tests for evaluate.py
    ###########################################################################

    @patch('evaluate.connect')
    @patch('evaluate.create_engine')
    # mock connect returns None. Did not use an underscore in the interest of
    # readibility.
    def test_run_evaluators_no_evals(self, mock_create_engine, mock_connect):
        mock_create_engine.return_value = Engine()
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators()
        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        expected = list()
        self.assertListEqual(expected, evaluator.statements)
        self.assertListEqual(expected, evaluator.metadata_statements)

    @patch('evaluate.connect')
    @patch('evaluate.create_engine')
    def test_run_evaluators_produces_results(self, mock_create_engine, mock_connect):
        # should correctly insert one statement and one metadata statement
        mock_create_engine.return_value = Engine()
        results = [{"id": "32", "date_created": "12312019",  "cons_acct_num": "0032", "field1": "value1", "field2": "value2", "field3": "value3"}]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["ID", "Date", "Acct", "Field 1", "Field 2", "Field 3"]
        )]
        evaluator.run_evaluators()
        self.assertEqual(1, len(evaluator.statements))
        self.assertEqual(1, len(evaluator.metadata_statements))

    @patch('evaluate.connect')
    @patch('evaluate.create_engine')
    def test_run_evaluators_invalid_results_raises_exception(self, mock_create_engine, mock_connect):
        # should raise an exception when there are less than 3 fields in
        # results and terminate the program with exit code 1
        mock_create_engine.return_value = Engine()
        results = [{"id": 1, "date_created": 2}]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["Field 1", "Field 2"]
        )]
        with self.assertRaises(SystemExit) as cm:
            evaluator.run_evaluators()

        self.assertEqual(cm.exception.code, 1)

    @patch('evaluate.connect')
    @patch('evaluate.create_engine')
    def test_write_results_executes_statements(self, mock_create_engine, mock_connect):
        mock_create_engine.return_value = Engine(
            connect_return=Connection()
        )
        # tests that evaluate statements are executed
        evaluator.statements = ["a valid statement"]
        evaluator.metadata_statements = list()
        with patch.object(Connection, 'execute') as mock:
            evaluator.write_results()
            mock.assert_called_with("a valid statement")

    @patch('evaluate.connect')
    @patch('evaluate.create_engine')
    def test_write_results_executes_metadata_statements(self, mock_create_engine, mock_connect):
        mock_create_engine.return_value = Engine(
            connect_return=Connection()
        )
        # tests that evaluate metadata statements are executed (these are executed after non-metadata statements)
        evaluator.statements = list()
        evaluator.metadata_statements = ["a valid metadata statement"]
        with patch.object(Connection, 'execute') as mock:
            evaluator.write_results()
            mock.assert_called_with("a valid metadata statement")

