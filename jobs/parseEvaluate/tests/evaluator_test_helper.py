import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from evaluate import evaluator
from tables import connect
from tests.fixtures import Dec_Base


###############################
# Setup and helper methods for testing evaluators
###############################
class TestM2Evaluators(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('postgresql+psycopg2://', creator=connect)
        # Delete all test data, in case previous tests didn't exit cleanly
        Dec_Base.metadata.drop_all(self.engine)
        self.session = Session(self.engine)
        Dec_Base.metadata.create_all(self.engine)

    def tearDown(self):
        Dec_Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def add_records_to_database(self, records):
        # Helper for preparing the test database
        for record in records:
            self.session.add(record)

        self.session.commit()

    def assert_evaluator_correct(self, eval_name: str, expected_result: list[tuple]):
        # Test that the evaluator:
        # 1. Name matches an evaluator in evaluators.py
        # 2. Is included in the list of evaluators to run
        # 3. Produces results in the expected format
        # 4. Triggers on the correct record
        evaluators_matching = 0
        for eval in evaluator.evaluators:
            if eval.name == eval_name:
                evaluators_matching += 1
                output = eval.exec_custom_func(connection=self.session, engine=self.engine)
                results = sorted(output, key=lambda x: x['id'])
        self.session.close()  # session.close must come before any assertions

        # Exactly one evaluator should have run
        self.assertEqual(evaluators_matching, 1)

        # compare expected result with actual result
        self.assertEqual(expected_result, results)
