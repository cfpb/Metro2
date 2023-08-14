import unittest

from evaluate import evaluator
from tests.fixtures import Engine, Evaluator, Connection, Res_Base, EvalResults

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from unittest.mock import patch



from tables import connect_res

class TestEvaluate(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql+psycopg2://', creator=connect_res)
        # Delete all test data, in case previous tests didn't exit cleanly+

        Res_Base.metadata.drop_all(self.engine)
        self.session = Session(self.engine)
        Res_Base.metadata.create_all(self.engine)

    def tearDown(self):
        Res_Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    # def add_records_to_database(self, records):
    #     # Helper for preparing the test database
    #     for record in records:
    #         self.session.add(record)

    #     self.session.commit()

    ###########################################################################
    # Tests for evaluate.py
    ###########################################################################

    # mock connect returns None. Did not use an underscore in the interest of
    # readibility.
    def test_run_evaluators_no_evals(self):
        # set empty evaluators list (should not run any evaluators)
        evaluator.evaluators = []
        evaluator.run_evaluators()
        # the expected outcome of not running evaluators should be
        # empty lists for results and metadata
        expected = list()
        self.assertListEqual(expected, evaluator.statements)
        self.assertListEqual(expected, evaluator.metadata_statements)

    def test_run_evaluators_produces_results(self):
        # should correctly insert one statement and one metadata statement
        results = [{"id": "32", "date_created": "12312019",  "cons_acct_num": "0032", "field1": "value1", "field2": "value2", "field3": "value3"}]
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["ID", "Date", "Acct", "Field 1", "Field 2", "Field 3"]
        )]
        evaluator.run_evaluators()
        self.assertEqual(1, len(evaluator.statements))
        self.assertEqual(1, len(evaluator.metadata_statements))

    def test_run_evaluators_invalid_results_raises_exception(self):
        # should raise an exception when there are less than 3 fields in
        # results and terminate the program with exit code 1
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
    def test_write_results_executes_statements(self, mock_create_engine, mock_connect):
        mock_create_engine.return_value = Engine(
            connect_return=Connection()
        )
        # tests that evaluate metadata statements are executed (these are executed after non-metadata statements)
        evaluator.statements = list()
        evaluator.metadata_statements = ["a valid metadata statement"]
        with patch.object(Connection, 'execute') as mock:
            evaluator.write_results()
            mock.assert_called_with("a valid metadata statement")

    def test_run_prepare_statements_adds_a_statement(self):
        # should correctly insert one statement
        results = [{"id": "32", "date_created": "12312019",  "cons_acct_num": "0032", "field1": "value1", "field2": "value2", "field3": "value3"}]
        expected = str("INSERT INTO evaluator_results (evaluator_name, date, field_values, record_id, acct_num) VALUES (:evaluator_name, :date, :field_values, :record_id, :acct_num)")
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["ID", "Date", "Acct", "Field 1", "Field 2", "Field 3"]
        )]
        evaluator.statements = list()
        evaluator.metadata_statements = list()

        self.assertEqual(0, len(evaluator.statements))
        evaluator.prepare_statements(evaluator.evaluators[0], results[0])

        self.assertEqual(0, len(evaluator.metadata_statements))
        self.assertEqual(1, len(evaluator.statements))
        self.assertEqual(expected, str(evaluator.statements[0]))
             

    def test_run_prepare_metadata_statements_adds_a_metadata_statement(self):
        # should correctly insert one metadata statement
        results = [{"id": "32", "date_created": "12312019",  "cons_acct_num": "0032", "field1": "value1", "field2": "value2", "field3": "value3"}]
        expected = str("INSERT INTO evaluator_metadata (evaluator_name, fields, hits) VALUES (:evaluator_name, :fields, :hits)")
        evaluator.evaluators = [Evaluator(custom_func_return=results,
            fields=["ID", "Date", "Acct", "Field 1", "Field 2", "Field 3"]
        )]
        evaluator.statements = list()
        evaluator.metadata_statements = list()

        self.assertEqual(0, len(evaluator.metadata_statements))
        evaluator.prepare_metadata_statements(evaluator.evaluators[0], results[0])

        self.assertEqual(0, len(evaluator.statements))
        self.assertEqual(1, len(evaluator.metadata_statements))
        self.assertEqual(expected, str(evaluator.metadata_statements[0]))
