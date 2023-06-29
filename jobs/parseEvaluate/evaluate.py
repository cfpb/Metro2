import json
import os
from sqlalchemy import create_engine, insert, Integer, Table, Column, String, MetaData
from tables import connect
from m2_evaluators import *

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


evaluators = [
    # eval_2_1A,
    # eval_2_2A,
    # eval_2_3A,
    # eval_2_4A,
    # eval_2_5A,
    # eval_2_6A,
    eval_6_4B,
    eval_prog_dofd_1,
    # eval_prog_status_1,
    eval_addl_apd_1,
    # eval_addl_doai_1,
    # eval_13_10B_1,
    # eval_13_10B_2,
    # eval_13_10B_3,
    # eval_7_21C_1,
    eval_7_21C_2,
    # eval_9_4A_1,
    # eval_9_4A_2,
    # eval_9_4A_3
]


class Evaluate():
    def __init__(self):
        self.evaluators = dict()
        self.results = dict()
        self.exam_number = 9999
        self.industry_type = ''
        self.date_format = '%m%d%Y'
        self.statements = list()
        self.metadata_statements = list()

    # outputs evaluators to json
    def run_evaluators(self, outpath):
        engine = None

        print("Connecting to PostgreSQL database...")
        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect)
            conn = engine.connect()

            # set exam globals
            # TODO: Test that this works. We might need to find another way to set these.
            if len(evaluators) > 0:
                evaluators[0].set_globals(self.industry_type, self.exam_number)

            # run evaluators
            for evaluator in evaluators:
                results = evaluator.exec_custom_func(connection=conn, engine=engine)

                # write to results
                if len(results) > 0:
                    try:
                        for row_data in results:
                            vals = ','.join(row_data[i] for i in range(3, len(evaluator.fields)))
                            self.statements.append(
                                insert(str(evaluator.name)).
                                values(
                                    date=row_data[1],
                                    record_id=row_data[0],
                                    acct_num=row_data[2],
                                    field_values=vals
                                )
                            )
                        # write to metadata table
                        self.metadata_statements.append(
                            insert('evaluator_metadata').
                            values(
                                evaluator_name=evaluator.name,
                                short_description=evaluator.description,
                                fields=evaluator.fields,
                                hits=len(results)
                            )
                        )
                    except Exception as e:
                        print("Unable to add result to results: ", e)
                        continue

        except Exception as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if engine is not None:
                engine.dispose()

    # connect to results database and write results
    def write_results(self):
        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect('metro2-results', 'results-db-postgresql', 5432))
            conn = engine.connect()

            # create tables in results database
            meta = MetaData()

            # create metadata table
            temp_meta = Table(
                'evaluator_metadata', meta,
                Column('evaluator_name', String(30)),
                Column('short_description', String(400)),
                Column('fields', String(400)),
                Column('hits', Integer)
            )

            temp_meta.create(engine)

            for evaluator in evaluators:
                temp_tbl = Table(
                    str(evaluator.name), meta,
                    Column('date', String(8)),
                    Column('field_values', String()),
                    Column('record_id', String(24)),
                    Column('acct_num', String(30))
                )

                temp_tbl.create(engine)

            # write to results database
            for stmt in self.statements:
                conn.execute(stmt)
            for meta in self.metadata_statements:
                conn.execute(meta)

        except Exception as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if engine is not None:
                engine.dispose()

# create instance of evaluator
evaluator = Evaluate()
