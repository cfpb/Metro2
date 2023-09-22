import os
import sys
import logging
import tempfile

import s3
from parse import Parser
from evaluate import evaluator
from tables import create_tables, engine
from envvar import fetch_env_var


ENABLE_S3 = fetch_env_var('ENABLE_S3', False)
LOGFILE_LOCATION = fetch_env_var('LOGFILE_LOCATION', "")


def init_db(db_engine):
    # init database tables
    create_tables(db_engine)

def parse(fstream, db_connection):
    # create a temporary parser for each file
    temp_parser = Parser()

    # parse file contents to working memory
    temp_parser.construct_commands(fstream)

    # write parsed data to database
    with db_connection.begin():
        cursor = db_connection.connection.cursor()
        temp_parser.exec_commands(cursor)

def parse_files_from_s3_bucket(db_connection):
    exam_root = fetch_env_var('S3_EXAM_ROOT')
    bucket = s3.getBucket()
    files = s3.list_objects(bucket, exam_root)
    logging.info(f"Finding all files in bucket matching prefix '{exam_root}'")
    for f in files:
        logging.debug(f"Encountered file in S3: {f.key}")
        try:
            # Unforunately, we can't stream files directly from S3 into the parser,
            # because S3 streambody objects don't have the seek() function, which
            # is used extensively in the parser. As a workaround, we temporarily
            # save the file to the local container, then read it from there into
            # the parser.

            # The file is streamed from S3 in 'bytes' mode
            temporary_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
            with temporary_file as tf:
                bucket.Object(f.key).download_fileobj(tf)
            logging.debug(f"Downloaded file {f.key} successfully.")

            # Open the file in 'text' mode for parsing
            with open(temporary_file.name, mode='r') as tf:
                parse(tf, db_connection)
            logging.info(f'File {f.key} written to database.')
        finally:
            os.remove(temporary_file.name)

def parse_files_from_local_filesystem(db_connection):
    local_exam_root = fetch_env_var('LOCAL_EXAM_ROOT')
    datafile_path = os.path.join(local_exam_root, "data")

    # iterate over files in [local_exam_root]/data/
    for filename in os.listdir(datafile_path):
        logging.debug(f"Encountered file in local data path: {filename}")
        # checking if the file is a .txt before proceeding
        if filename.lower().endswith('.txt'):
            file = os.path.join(datafile_path, filename)
            # checking if it is a file
            if os.path.isfile(file):
                try:
                    logging.debug(f"Parsing local file: {filename}")
                    fstream = open(file, 'r')
                    parse(fstream, db_connection)
                    logging.info(f'File {os.path.basename(fstream.name)} written to database.')
                except FileNotFoundError as e:
                    logging.error(f"There was an error opening the file: {e}")
                finally:
                    if fstream:
                        fstream.close()

def evaluate():
    evaluator.run_evaluators()
    logging.info(f'Evaluators run for exam. Hits written to database.')

def run():
    logging.basicConfig(
        # output file
        filename=os.path.join(LOGFILE_LOCATION, 'info.log'),
        # append instead of overwrite
        filemode='a',
        # message format
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        # date format (removed, to specify, uncomment the next line)
        # datefmt=
        # minimum message level that will be written
        # levels are: DEBUG, INFO, WARN, ERROR, FATAL
        level=logging.DEBUG
    )
    db_engine = engine()
    init_db(db_engine)
    db_connection = db_engine.connect()

    if ENABLE_S3:
        logging.info("ENABLE_S3 set. Reading files from S3 bucket.")
        parse_files_from_s3_bucket(db_connection)
    else:
        logging.info("ENABLE_S3 env var not set. Reading files from local data directory.")
        parse_files_from_local_filesystem(db_connection)

    # TODO: uncomment the evaluate command when we are ready to troubleshoot evaluators
    # evaluate()

    # After all DB transactions are finished, close the DB engine.
    db_engine.dispose()

run()
