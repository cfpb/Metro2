import os
import sys

from sqlalchemy import create_engine, insert
from tables import connect, meta_tbl, res_tbl
from m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from m2_evaluators.cat7_evals import evaluators as cat7_evals
from m2_evaluators.cat12_evals import evaluators as cat12_evals
from psycopg2 import OperationalError
from logger import getLogger


class Evaluate():
    def __init__(self):
        #  When evaluators are provided by additional files, add them here
        #   e.g. self.evaluators = cat7_evals + cat9_evals + ...
        self.evaluators = addl_dofd_evals + cat7_evals + cat12_evals
        self.results = dict()
        self.date_format = '%m%d%Y'
        self.statements = list()
        self.metadata_statements = list()


    # runs evaluators to produce results
    def run_evaluators(self):
        logger = getLogger('evaluate.run_evaluators')
        engine = None

        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect)
            conn = engine.connect()

            # run evaluators
            for evaluator in self.evaluators:
                results = evaluator.exec_custom_func(connection=conn, engine=engine)
                # Generate insert statements for results, to be executed in write_results()
                if results:
                    try:
                        for row_data in results:
                            self.prepare_statements(evaluator, row_data)

                        # prepare metadata
                        self.prepare_metadata_statements(evaluator, results)

                    except KeyError as e:
                        logger.error(f"Unable to add result to results: {e}")
                        # this should only be raised by a developer error
                        # so we want to exit.
                        sys.exit(1)

        except OperationalError as e:
            logger.error(f"There was a problem establishing the connection: {e}")
        finally:
            if engine is not None:
                engine.dispose()

    # connect to results database and write results
    def write_results(self):
        logger = getLogger('evaluate.write_results')
        engine = None

        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect)
            conn = engine.connect()

            # write to results database
            for stmt in self.statements:
                conn.execute(stmt)
            for meta in self.metadata_statements:
                conn.execute(meta)

        except OperationalError as e:
            logger.error(f"There was a problem establishing the connection: {e}")
        finally:
            if engine is not None:
                engine.dispose()

    def prepare_statements(self, evaluator, data):
        self.statements.append(
        insert(res_tbl).
        values(
            evaluator_name=evaluator.name,
            date=data['activity_date'],
            record_id=data['id'],
            acct_num=data['cons_acct_num'],
            field_values=data
            )
        )

    def prepare_metadata_statements(self, evaluator, data):
        # write to metadata table
        self.metadata_statements.append(
            insert(meta_tbl).
            values(
                evaluator_name=evaluator.name,
                hits=len(data)
            )
        )

# create instance of evaluator
evaluator = Evaluate()
