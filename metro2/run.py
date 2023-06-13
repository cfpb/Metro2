from metro2.parse import Parser
from metro2.evaluate import evaluator
import os

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

# retrieve environment variables. Throw exception if not found.
try:
    EXAM_ROOT = os.environ['EXAM_ROOT']
    EXAM_NUMBER = os.environ['EXAM_NUMBER']
    IND_TYPE_CODE = os.environ['INDUSTRY_TYPE_CODE']
except KeyError as e:
    print("Postgres connection variable(s) not found: ", e)
    exit(1)
except:
    print("Unexpected error, quitting...")
    exit(1)

RESULTFILE_PATH = os.path.join("results", "results.json")
DATAFILE_PATH = os.path.join(EXAM_ROOT, "data")
MAPFILE_PATH = os.path.join(EXAM_ROOT, "reference", "sample-map.xlsx")
SHEET_NAME = "Mapping"
COL_SEGMENT = "B"
COL_START = "F"
COL_END = "G"
COL_FIELDS = "I"
PII_FIELDS = list([
    "surname",
    "surname_j1",
    "surname_j2",
    "middle_name",
    "middle_name_j1",
    "middle_name_j2",
    "ssn",
    "ssn_j1",
    "ssn_j2",
    "dob",
    "dob_j1",
    "dob_j2",
    "addr_line_1",
    "addr_line_1_j2",
    "addr_line_2",
    "addr_line_2_j2",
    "zip",
    "zip_j2",
])

def init_db():
    # init database tables
    print(f'Initializing database tables for exam {EXAM_NUMBER}')
    temp_parser = Parser()
    temp_parser.create_tables()

def parse(filename, file):
    # create a temporary parser for each file
    temp_parser = Parser()
    temp_parser.map_fields(MAPFILE_PATH, SHEET_NAME, COL_SEGMENT, COL_START, COL_END, COL_FIELDS, PII_FIELDS)
    # write file contents to database
    print(f'Parsing file {filename}')
    temp_parser.construct_commands(file)
    print(f'Writing file {filename} to database')
    temp_parser.exec_commands(temp_parser.header_values, "header")
    temp_parser.exec_commands(temp_parser.trailer_values, "trailer")
    temp_parser.exec_commands(temp_parser.base_values, "base")
    temp_parser.exec_commands(temp_parser.J1_values, "j1")
    temp_parser.exec_commands(temp_parser.J2_values, "j2")
    temp_parser.exec_commands(temp_parser.K1_values, "k1")
    temp_parser.exec_commands(temp_parser.K2_values, "k2")
    temp_parser.exec_commands(temp_parser.K3_values, "k3")
    temp_parser.exec_commands(temp_parser.K4_values, "k4")
    temp_parser.exec_commands(temp_parser.L1_values, "l1")
    temp_parser.exec_commands(temp_parser.N1_values, "n1")
    print(f'File {filename} written to database')

def run():
    init_db()
    # iterate over data directory
    for filename in os.listdir(DATAFILE_PATH):
        file = os.path.join(DATAFILE_PATH, filename)
        # checking if it is a file
        if os.path.isfile(file):
            parse(filename, file)

    evaluator.exam_number = EXAM_NUMBER
    evaluator.industry_type = IND_TYPE_CODE
    print("Running evaluators...")
    evaluator.run_evaluators(RESULTFILE_PATH)
    print("Done!")

run()
