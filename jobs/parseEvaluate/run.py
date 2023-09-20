import os
import sys
import logging

from parse import Parser
from evaluate import evaluator
from tables import create_tables, engine

# retrieve environment variables. Throw exception if not found.
try:
    EXAM_ROOT = os.environ['EXAM_ROOT']
    EXAM_NUMBER = os.environ['EXAM_NUMBER']
except KeyError as e:
    logging.error(f"Postgres connection variable(s) not found: {e}")
    sys.exit(1)

DATAFILE_PATH = os.path.join(EXAM_ROOT, "data")

def init_db(db_engine):
    # init database tables
    create_tables(db_engine)
    logging.info(f'Initialized database tables for exam {EXAM_NUMBER}')

def parse(fstream, db_connection):
    # create a temporary parser for each file
    temp_parser = Parser()

    # parse file contents to working memory
    temp_parser.construct_commands(fstream)

    # write parsed data to database
    with db_connection.begin():
        cursor = db_connection.connection.cursor()
        temp_parser.exec_commands(cursor)

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
    db_engine = engine()
    init_db(db_engine)
    db_connection = db_engine.connect()

    # iterate over data directory
    for filename in os.listdir(DATAFILE_PATH):
        logging.debug(f"Encountered file in local data path: {filename}")
        # checking if the file is a .txt before proceeding
        if filename.lower().endswith('.txt'):
            file = os.path.join(DATAFILE_PATH, filename)
            # checking if it is a file
            if os.path.isfile(file):
                try:
                    logging.debug(f"Parsing local file: {filename}")
                    fstream = open(file, 'r')
                    parse(fstream, db_connection)
                except FileNotFoundError as e:
                    logging.error(f"There was an error opening the file: {e}")
                finally:
                    if fstream:
                        fstream.close()
    # TODO: uncomment the evaluate command when we are ready to troubleshoot evaluators
    # evaluate()

    # After all DB transactions are finished, close the DB engine.
    db_engine.dispose()

run()
