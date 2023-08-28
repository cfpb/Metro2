import os
import sys
import logging

from parse import Parser
from evaluate import evaluator
from tables import create, meta, res_meta

# check if tool is set to run locally
try:
    METRO2ENV = os.environ['METRO2ENV']
except KeyError as e:
    logging.error("Environment (local, prod, etc.) not found: %s", e)
    sys.exit(1)
except:
    logging.error("Unexpected error, quitting...")
    sys.exit(1)

# quit if not local
if METRO2ENV != 'local':
    logging.error("Metro2 evaluator tool is not configured to run in production. \
        Quitting...")
    sys.exit(1)

# retrieve environment variables. Throw exception if not found.
try:
    EXAM_ROOT = os.environ['EXAM_ROOT']
    EXAM_NUMBER = os.environ['EXAM_NUMBER']
except KeyError as e:
    logging.error("Postgres connection variable(s) not found: ", e)
    sys.exit(1)
except:
    logging.error("Unexpected error, quitting...")
    sys.exit(1)

DATAFILE_PATH = os.path.join(EXAM_ROOT, "data")

def init_db():
    # init database tables
    create(meta)
    create(res_meta)
    logging.info(f'Initialized database tables for exam {EXAM_NUMBER}')

def parse(fstream):
    # create a temporary parser for each file
    temp_parser = Parser()
    # write file contents to database
    temp_parser.construct_commands(fstream)
    temp_parser.exec_commands()
    logging.info(f'File {os.path.basename(fstream.name)} written to database')

def evaluate():
    evaluator.exam_number = EXAM_NUMBER
    evaluator.run_evaluators()
    logging.info(f'Evaluators run for exam {EXAM_NUMBER}. Hits written to database.')

def run():
    logging.basicConfig(
        # output file
        filename=os.path.join(EXAM_ROOT, 'info.log'),
        # append instead of overwrite
        filemode='a',
        # message format
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        # date format (removed, to specify, uncomment the next line)
        # datefmt=
        # minimum message level that will be written
        # levels are: 
        # DEBUG,
        # INFO,
        # WARN,
        # ERROR,
        # FATAL
        level=logging.DEBUG
    )
    init_db()
    # iterate over data directory
    for filename in os.listdir(DATAFILE_PATH):
        file = os.path.join(DATAFILE_PATH, filename)
        # checking if it is a file
        if os.path.isfile(file):
            try:
                fstream = open(file, 'r')
                parse(fstream)
            except FileNotFoundError as e:
                logging.error("There was an error opening the file: ", e)
            finally:
                if fstream:
                    fstream.close()
    evaluate()

run()
