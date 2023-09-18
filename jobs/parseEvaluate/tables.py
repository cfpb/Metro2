import psycopg2
import os
import sys
import logging

from sqlalchemy import(
    create_engine,
    MetaData,
    Table,
    Column,
    ForeignKey,
    JSON,
    Integer,
    SmallInteger,
    String
)

# retrieve environment variables. Throw exception if not found.
try:
    PGHOST = os.environ['PGHOST']
    PGPORT = os.environ['PGPORT']
    PGDATABASE = os.environ['PGDATABASE']
    PGUSER = os.environ['PGUSER']
    PGPASSWORD = os.environ['PGPASSWORD']
except KeyError as e:
    logging.error(f"Postgres connection variable(s) not found: {e}")
    sys.exit(1)

##############################################
# Parsed data
##############################################
meta = MetaData()

header = Table(
    'header', meta,
    Column('id', String(24)),
    Column('file', String(24), unique=True),
    Column('rdw_header', SmallInteger),
    Column('record_identifer_header', String(6)),
    Column('cycle_identifier_header', String(2)),
    Column('innovis_program_identifier', String(10)),
    Column('equifax_program_identifier', String(10)),
    Column('experian_program_identifier', String(5)),
    Column('transunion_program_identifier', String(10)),
    Column('activity_date', String(8)),
    Column('date_created', String(8)),
    Column('program_date', String(8)),
    Column('program_revision_date', String(8)),
    Column('reporter_name', String(40)),
    Column('reporter_address', String(96)),
    Column('reporter_telephone_number', String(10)),
    Column('software_vendor_name', String(40)),
    Column('software_version_number', String(5)),
    Column('microbilt_prbc_program_identifier', String(10)),
    Column('reserved_header', String(146))
)

base = Table(
    'base', meta,
    Column('id', String(24),  unique=True),
    Column('file', String(24), ForeignKey("header.file")),
    Column('rdw', SmallInteger),
    Column('proc_ind', String(1)),
    Column('time_stamp', String(8)),
    Column('throw_out_hms', String(6)),
    Column('reserved_base', String(1)),
    Column('id_num', String(20)),
    Column('cycle_id', String(2)),
    Column('cons_acct_num', String(30)),
    Column('port_type', String(1)),
    Column('acct_type', String(2)),
    Column('date_open', String(8)),
    Column('credit_limit', String(9)),
    Column('hcola', String(9)),
    Column('terms_dur', String(3)),
    Column('terms_freq', String(1)),
    Column('smpa', String(9)),
    Column('actual_pmt_amt', String(9)),
    Column('acct_stat', String(2)),
    Column('pmt_rating', String(1)),
    Column('php', String(24)),
    Column('spc_com_cd', String(2)),
    Column('compl_cond_cd', String(2)),
    Column('current_bal', String(9)),
    Column('amt_past_due', String(9)),
    Column('orig_chg_off_amt', String(9)),
    Column('doai', String(8)),
    Column('dofd', String(8)),
    Column('date_closed', String(8)),
    Column('dolp', String(8)),
    Column('int_type_ind', String(1)),
    Column('reserved_base_2', String(17)),
    Column('surname', String(25)),
    Column('first_name', String(20)),
    Column('middle_name', String(20)),
    Column('gen_code', String(1)),
    Column('ssn', String(9)),
    Column('dob', String(8)),
    Column('phone_num', String(10)),
    Column('ecoa', String(1)),
    Column('cons_info_ind', String(2)),
    Column('country_cd', String(2)),
    Column('addr_line_1', String(32)),
    Column('addr_line_2', String(32)),
    Column('city', String(20)),
    Column('state', String(2)),
    Column('zip', String(9)),
    Column('addr_ind', String(1)),
    Column('res_cd', String(1))
)

j1 = Table(
    'j1', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('segment_identifier_j1', String(2)),
    Column('reserved_j1', String(1)),
    Column('surname_j1', String(25)),
    Column('first_name_j1', String(20)),
    Column('middle_name_j1', String(20)),
    Column('gen_code_j1', String(1)),
    Column('ssn_j1', String(9)),
    Column('dob_j1', String(8)),
    Column('phone_num_j1', String(10)),
    Column('ecoa_j1', String(1)),
    Column('cons_info_ind_j1', String(2)),
    Column('reserved_j1_2', String(1))
)

j2 = Table(
    'j2', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('segment_identifier_j2', String(2)),
    Column('reserved_j2', String(1)),
    Column('surname_j2', String(25)),
    Column('first_name_j2', String(20)),
    Column('middle_name_j2', String(20)),
    Column('gen_code_j2', String(1)),
    Column('ssn_j2', String(9)),
    Column('dob_j2', String(8)),
    Column('phone_num_j2', String(10)),
    Column('ecoa_j2', String(1)),
    Column('cons_info_ind_j2', String(2)),
    Column('country_cd_j2', String(2)),
    Column('addr_line_1_j2', String(32)),
    Column('addr_line_2_j2', String(32)),
    Column('city_j2', String(20)),
    Column('state_j2', String(2)),
    Column('zip_j2', String(9)),
    Column('addr_ind_j2', String(1)),
    Column('res_cd_j2', String(1)),
    Column('reserved_j2_2', String(2))
)

k1 = Table(
    'k1', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('K1_seg_id', String(2)),
    Column('K1_orig_creditor_name', String(30)),
    Column('K1_creditor_classification', String(2))
)

k2 = Table(
    'k2', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('k2_seg_id', String(2)),
    Column('k2_purch_sold_ind', String(1)),
    Column('k2_purch_sold_name', String(30)),
    Column('reserved_k2', String(1))
)

k3 = Table(
    'k3', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('k3_seg_id', String(2)),
    Column('k3_agcy_id', String(2)),
    Column('k3_agcy_acct_num', String(18)),
    Column('k3_min', String(18))
)

k4 = Table(
    'k4', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('k4_seg_id', String(2)),
    Column('k4_spc_pmt_ind', String(2)),
    Column('k4_deferred_pmt_st_dt', String(8)),
    Column('k4_balloon_pmt_due_dt', String(8)),
    Column('k4_balloon_pmt_amt', String(9)),
    Column('reserved_k4', String(1))
)

l1 = Table(
    'l1', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('l1_seg_id', String(2)),
    Column('l1_change_ind', String(1)),
    Column('l1_new_acc_num', String(30)),
    Column('l1_new_id_num', String(20)),
    Column('reserved_l1', String(1))
)

n1 = Table(
    'n1', meta,
    Column('id', String(24), ForeignKey("base.id")),
    Column('file', String(24)),
    Column('n1_seg_id', String(2)),
    Column('n1_employer_name', String(30)),
    Column('employer_addr1', String(32)),
    Column('employer_addr2', String(32)),
    Column('employer_city', String(20)),
    Column('employer_state', String(2)),
    Column('employer_zip', String(9)),
    Column('occupation', String(18)),
    Column('reserved_n1', String(1))
)

trailer = Table(
    'trailer', meta,
    Column('id', String(24)),
    Column('file', String(24), ForeignKey("header.file")),
    Column('rdw_trailer', Integer),
    Column('record_identifer_trailer', String(7)),
    Column('total_base_records', String(9)),
    Column('reserved_trailer', String(9)),
    Column('total_status_df', String(9)),
    Column('total_j1_segments', String(9)),
    Column('total_j2_segments', String(9)),
    Column('block_count', String(9)),
    Column('total_status_da', String(9)),
    Column('reserved_trailer_2', String(9)),
    Column('total_status_11', String(9)),
    Column('total_status_13', String(9)),
    Column('total_status_61', String(9)),
    Column('total_status_62', String(9)),
    Column('total_status_63', String(9)),
    Column('total_status_64', String(9)),
    Column('total_status_65', String(9)),
    Column('total_status_71', String(9)),
    Column('total_status_78', String(9)),
    Column('total_status_80', String(9)),
    Column('total_status_82', String(9)),
    Column('total_status_83', String(9)),
    Column('total_status_84', String(9)),
    Column('total_status_88', String(9)),
    Column('total_status_89', String(9)),
    Column('total_status_93', String(9)),
    Column('total_status_94', String(9)),
    Column('total_status_95', String(9)),
    Column('total_status_96', String(9)),
    Column('total_status_97', String(9)),
    Column('total_ecoa_z', String(9)),
    Column('total_employment_segments', String(9)),
    Column('total_original_creditor_segments', String(9)),
    Column('total_purchased_sold_segments', String(9)),
    Column('total_mortgage_segments', String(9)),
    Column('total_special_payment_segments', String(9)),
    Column('total_change_segments', String(9)),
    Column('total_ssn', String(9)),
    Column('total_ssn_base', String(9)),
    Column('total_ssn_j1', String(9)),
    Column('total_ssn_j2', String(9)),
    Column('total_dob', String(9)),
    Column('total_dob_base', String(9)),
    Column('total_dob_j1', String(9)),
    Column('total_dob_j2', String(9)),
    Column('total_phone_numbers', String(9)),
    Column('reserved_trailer_3', String(19))
)

##############################################
# Results data
##############################################

meta_tbl = Table(
    'evaluator_metadata', meta,
    Column('evaluator_name', String(200), unique=True),
    Column('hits', Integer)
)

res_tbl = Table(
    'evaluator_results', meta,
    Column('evaluator_name', String(200)),
    Column('date', String(8)),
    Column('field_values', JSON),
    Column('record_id', String(24), unique=True),
    Column('acct_num', String(30))
)

# establishes a database connection using psycopg2.
def connect():
    return psycopg2.connect(
        host=PGHOST,
        port=PGPORT,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD
    )

##############################################
# Shared helper methods
##############################################
# creates tables defined above. Medatadata must be specified.
# If no creator is specified, sqlalchemy will use the connect
# method for PGDATABASE.
def create(metadata, creator=connect):
    engine = None

    try:
        engine = create_engine('postgresql+psycopg2://', creator=creator)
        # create all tables defined above
        metadata.create_all(engine)

    except Exception as e:
        logging.error(f"There was a problem establishing the connection: {e}")
    finally:
        if engine is not None:
            engine.dispose()
