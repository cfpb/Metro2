import unittest

from evaluate import evaluator
from tests.fixtures import Engine, ExpectedException, Evaluator, Connection
from unittest.mock import patch

class TestEvaluate(unittest.TestCase):

    ###########################################################################
    # Tests for evaluate.py
    ###########################################################################

    @patch('sqlalchemy.create_engine')
    @patch('tables.connect')
    def test_run_evaluators_no_evals(self, mock_create_engine, mock_connect):
        mock_create_engine.return_value = Engine()
        mock_connect.return_value = None
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators()
        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        expected = list()
        self.assertListEqual(expected, evaluator.statements)
        self.assertListEqual(expected, evaluator.metadata_statements)

    @patch('sqlalchemy.create_engine')
    @patch('tables.connect')
    def test_run_evaluators_set_globals_called(self, mock_create_engine, mock_connect):
        # mocks calls that happen within the run_evaluators function to
        # trigger an exception and assert that set_globals and dispose were
        # called
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException()
        )
        mock_connect.return_value = None
        evaluator.evaluators = [Evaluator(set_globals_return=Exception())]
        self.assertRaises(ExpectedException, evaluator.run_evaluators)

    @patch('sqlalchemy.create_engine')
    @patch('tables.connect')
    def test_run_evaluators_produces_results(self, mock_create_engine, mock_connect):
        # should correctly insert one statement and one metadata statement
        mock_create_engine.return_value = Engine()
        mock_connect.return_value = None
        results = [1, 2, 3, [1, 2]]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["Field 1", "Field 2"]
        )]
        self.assertEqual(1, len(evaluator.statements))
        self.assertEqual(1, len(evaluator.metadata_statements))

    @patch('sqlalchemy.create_engine')
    @patch('tables.connect')
    def test_run_evaluators_invalid_results_raises_exception(self, mock_create_engine, mock_connect):
        # should raise an exception when there are less than 3 fields in
        # results
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException()
        )
        mock_connect.return_value = None
        results = [1, 2]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["Field 1", "Field 2"]
        )]
        self.assertRaises(ExpectedException, evaluator.run_evaluators)

    @patch('sqlalchemy.create_engine')
    @patch('sqlalchemy.Table.create')
    @patch('tables.connect')
    def test_write_results_executes_statements(self, mock_create_engine, mock_table_create, mock_connect):
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException(),
            connect_return=Connection(
                execute_return=Exception()
            )
        )
        mock_table_create.return_value = None
        mock_connect.return_value = None
        # tests that evaluate statements are executed
        evaluator.statements = ["a valid statement"]
        self.assertRaises(ExpectedException, evaluator.write_results)

    @patch('sqlalchemy.create_engine')
    @patch('sqlalchemy.Table.create')
    @patch('tables.connect')
    def test_write_results_executes_metadata_statements(self, mock_create_engine, mock_table_create, mock_connect):
        mock_create_engine.return_value = Engine(
            dispose_return=ExpectedException(),
            connect_return=Connection(
                execute_return=Exception()
            )
        )
        mock_table_create.return_value = None
        mock_connect.return_value = None
        # tests that evaluate metadata statements are executed (these are executed after non-metadata statements)
        evaluator.metadata_statements = ["a valid metadata statement"]
        self.assertRaises(ExpectedException, evaluator.write_results)

