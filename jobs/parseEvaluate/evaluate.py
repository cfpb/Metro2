import os
import sys

from sqlalchemy import create_engine, insert, Integer, Table, Column, String, MetaData
from tables import connect, meta_tbl, res_tbl, connect_res
from m2_evaluators.cat7_evals import evaluators as cat7_evals
from psycopg2 import OperationalError

# check if tool is set to run locally
try:
    METRO2ENV = os.environ['METRO2ENV']
except KeyError as e:
    print("Environment (local, prod, etc.) not found: %s", e)
    exit(1)
except:
    print("Unexpected error, quitting...")
    exit(1)

# quit if not local
if METRO2ENV != 'local':
    print("Metro2 evaluator tool is not configured to run in production. \
        Quitting...")
    exit(1)


class Evaluate():
    def __init__(self):
        self.evaluators = cat7_evals  #  When evaluators are provided by additional files, add them here
                                      #   e.g. self.evaluators = cat7_evals + cat9_evals + ...
        self.results = dict()
        self.exam_number = 9999
        self.industry_type = ''
        self.date_format = '%m%d%Y'
        self.statements = list()
        self.metadata_statements = list()

    # runs evaluators to produce results
    def run_evaluators(self):
        engine = None

        print("Connecting to PostgreSQL database...")
        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect)
            conn = engine.connect()

            # set exam globals
            # TODO: Test that this works. We might need to find another way to set these.
            if len(self.evaluators) > 0:
                self.evaluators[0].set_globals(self.industry_type, self.exam_number)

            # run evaluators
            for evaluator in self.evaluators:
                results = evaluator.exec_custom_func(connection=conn, engine=engine)

                # Generate insert statements for results, to be executed in write_results()
                if results:
                    try:
                        for row_data in results:
                            vals = ','.join(str(row_data[i]) for i in range(3, len(evaluator.fields)))
                            self.statements.append(
                                insert(res_tbl).
                                values(
                                    evaluator_name=evaluator.name,
                                    date=row_data[1],
                                    record_id=row_data[0],
                                    acct_num=row_data[2],
                                    field_values=vals
                                )
                            )
                        # write to metadata table
                        self.metadata_statements.append(
                            insert(meta_tbl).
                            values(
                                evaluator_name=evaluator.name,
                                fields=evaluator.fields,
                                hits=len(results)
                            )
                        )
                    except IndexError as e:
                        print("Unable to add result to results: ", e)
                        # this exception should only be raised as a result of
                        # something a developer broke, so we don't want to
                        # continue execution.
                        sys.exit(1)

        except OperationalError as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if engine is not None:
                engine.dispose()

    # connect to results database and write results
    def write_results(self):
        engine = None
        
        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect_res)
            conn = engine.connect()

            # write to results database
            for stmt in self.statements:
                conn.execute(stmt)
            for meta in self.metadata_statements:
                conn.execute(meta)

        except OperationalError as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if engine is not None:
                engine.dispose()

# create instance of evaluator
evaluator = Evaluate()
