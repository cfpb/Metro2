import json
import os
from metro2.tables import connect
from metro2.evaluator import evaluators
from sqlalchemy import create_engine

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

    # reads in a JSON file and stores the data in memory
    def load_json(self, path):
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
        description = 'description'
        data = 'data'
        hits = 'hits'
        date = 'date'
        fields = 'fields'

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
                sel = evaluator.exec_custom_func()
                if sel is not None:
                    res = conn.execute(sel)
                    for row in res:
                        results.append(list(row))
                    
                    # write to results
                    if len(results) > 0:
                        data_dict = {}
                        try:
                            data_dict = {row_data[0]: {date: row_data[1], fields: row_data[2:]} for row_data in results}
                        except Exception as e:
                            print("Unable to add data: ", e)
                            continue
                        self.results[evaluator.name] = {
                            description: evaluator.description,
                            data: data_dict,
                            hits: len(results)
                        }

            # write results to json
            self.write_json(outpath, self.results)

        except Exception as e:
            print("There was a problem establishing the connection: ", e)
        finally:
            if engine is not None:
                engine.dispose()

# create instance of evaluator
evaluator = Evaluate()
