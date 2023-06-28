import json
import os
from tables import connect
from evaluator import evaluators
from sqlalchemy import create_engine, insert, Integer, Table, Column, String, MetaData

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
        self.evaluators = dict()
        self.results = dict()
        self.exam_number = 9999
        self.industry_type = ''
        self.date_format = '%m%d%Y'
        self.statements = list()
        self.metadata_statements = list()

    # reads in a JSON file and stores the data in memory
    def load_json(self, path):
        file = None
        try:
            file = open(path, "r")
            self.evaluators = json.load(file)
        except FileNotFoundError as e:
            print("Invalid file name for loading JSON: ", e)
            exit(1)
        finally:
            if file is not None:
                file.close()

    # writes evaluators to file
    def write_json(self, path, data):
        file = None
        try:
            file = open(path, "w")
            json.dump(data, file, indent=4)
        except FileNotFoundError as e:
            print("Path does not exist: ", e)
            exit(1)
        finally:
            if file is not None:
                file.close()

    # adds a custom evaluator given an evaluator name, and dictionaries
    # containing fields and inverse fields.
    def add_custom_evaluator(self, path, name, content):
        criteria = "criteria"
        self.load_json(path)
        # check to make sure an existing evaluator will not be overwritten.
        if name not in self.evaluators[criteria]:
            self.evaluators[criteria][name] = {
                content
            }

        # write to file
        self.write_json(path, self.evaluators)

    # outputs evaluators to json
    def run_evaluators(self, outpath):
        engine = None

        print("Connecting to PostgreSQL database...")
        try:
            engine = create_engine('postgresql+psycopg2://', creator=connect)
            conn = engine.connect()

            # set exam globals
            if len(evaluators) > 0:
                evaluators[0].set_globals(self.industry_type, self.exam_number)

            # run evaluators
            for evaluator in evaluators:
                # execute evaluator code
                results = list()
                res = None
                if evaluator.longitudinal_func:
                    res = evaluator.exec_custom_func(connection=conn, engine=engine)
                    results = res
                else:
                    sel = evaluator.exec_custom_func()
                    if sel is not None:
                        res = conn.execute(sel)
                        for row in res:
                            results.append(list(row))

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
