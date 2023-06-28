# defines the evaluator class and list of evaluators

from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, func, cast, Integer, Table, Column, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, literal
from iterator_file import IteratorFile
from tables import (
    connect,
    header,
    base,
    j1,
    j2,
    k1,
    k2,
    k3,
    k4,
    l1,
    n1,
    trailer
)

exam_number = 9999
industry_type = ''
date_format = 'MMDDYYYY'
strptime_format = '%m%d%Y'

class Evaluator():
    def __init__(self, name, description, fields, func=None, longitudinal_func=None):
        self.name = name
        self.description = description
        self.fields = fields
        self.func = func
        self.longitudinal_func = longitudinal_func

    def set_globals(self, ind_type, exam_num):
        exam_number = exam_num
        industry_type = ind_type

    def exec_custom_func(self, connection=None, engine=None):
        # returns a list of results from running a query
        if self.longitudinal_func:
            res_set = self.longitudinal_func(connection, engine)

            # if a temporary table was created in getting results, delete it here.
            try:
                base = declarative_base()
                metadata = MetaData(engine, reflect=True)
                table = metadata.tables.get('temp_tbl')
                if table is not None:
                    print("Deleting temp table...")
                    base.metadata.drop_all(engine, [table], checkfirst=True)
            except Exception as e:
                print("There was an issue getting or deleting temp table: ", e)

        else:
            res = connection.execute(self.func())

            res_set = list()

            for result in res:
                res_set.append(result)

        return res_set

# evaluators to run
eval_2_1A = Evaluator(
    "2-1A",
    "Portfolio type does not match the industry type, 'Bank' or 'Credit Union'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['C', 'I', 'M', 'O', 'R'])
        )
    ) if(industry_type in ["B", "CU"]) else None)
)

eval_2_2A = Evaluator(
    "2-2A",
    "Portfolio type does not match the industry type, 'Finance Company'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['C', 'I', 'O', 'R'])
        )
    ) if(industry_type in ["FC"]) else None)
)

eval_2_3A = Evaluator(
    "2-3A",
    "Portfolio type does not match the industry type, 'Mortgage Lender'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['C', 'I', 'M'])
        )
    ) if(industry_type in ["M"]) else None)
)

eval_2_4A = Evaluator(
    "2-4A",
    "Portfolio type does not match the industry type, 'Credit Card'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['C', 'O', 'R'])
        )
    ) if(industry_type in ["CC"]) else None)
)

eval_2_5A = Evaluator(
    "2-5A",
    "Portfolio type does not match the industry type, 'Sales Finance' or 'Retail Store'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['I', 'R'])
        )
    ) if(industry_type in ["SF", "RS"]) else None)
)

eval_2_6A = Evaluator(
    "2-6A",
    "Portfolio type does not match the industry type, 'Collection Agency' or 'Debt Buyer'",
    ['database record id', 'date created', 'consumer account number', 'portfolio type'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.port_type).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.port_type.in_(['O'])
        )
    ) if(industry_type in ["CI"]) else None)
)

eval_6_4B = Evaluator(
    "6-4B",
    "This is an account that has not been paid or transferred, has a current balance, and no deferred terms frequency, but has a balloon payment due date.",
    ['database record id', 'date created', 'consumer account number', 'account status', 'terms frequency', 'current balance', 'k4 balloon payment due date'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.terms_freq, base.c.current_bal, k4.c.k4_balloon_pmt_due_dt).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == k4.c.id,
            ~base.c.acct_stat.in_(['05', '13', '61', '62', '63', '64', '65']),
            base.c.terms_freq != 'D',
            cast(base.c.current_bal, Integer) > 0,
            ~k4.c.k4_balloon_pmt_due_dt.in_(['00000000','        ', ''])
        )
    ))
)

def eval_prog_dofd_1_func(connection, engine):
    res = connection.execute(select(header.c.date_created, base.c.dofd, base.c.cons_acct_num, base.c.acct_stat).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat.in_(['61', '62', '63', '64', '65', '71', '78', '80', '82', '83', '84', '93', '94', '95', '96', '97'])
        )
    ))
    res_set = list()

    print("first query done")

    meta = MetaData()

    temp_tbl = Table(
        'temp_tbl', meta,
        Column('compare_date', String(8)),
        Column('prior_dofd', String(8)),
        Column('prior_acct_num', String(30)),
        Column('prior_acct_stat', String(2)),
    )
    
    temp_tbl.create(engine)

    for prev_date_created, dofd, acct_num, acct_stat in res:
        compare_date = datetime.strptime(prev_date_created, strptime_format) + relativedelta(months=+1)
        compare_date_str = compare_date.strftime(strptime_format)
        result = list([str(compare_date_str), str(dofd), str(acct_num), str(acct_stat)])
        res_set.append(result)

    print("set created")

    conn = None
    # create a new connection and cursor using just psycopg2 (not SQLAlchemy)
    try:
        conn = connect()
        cur = conn.cursor()

        block_start = 0
        block_size = 2000
        tup_set = tuple(res_set)
        sub = list()
        sub.append('{}')
        # the length of each result will be the same.
        commands = '\t'.join(sub * (len(tup_set[block_start])))

        while (block_start + block_size) < len(tup_set):
            block_end = block_start + block_size
            # split values
            val_list = tup_set[block_start:block_end]

            copy = IteratorFile((commands.format(*vals) for vals in val_list))

            cur.copy_from(copy, 'temp_tbl')
            # persist changes
            conn.commit()

            block_start += block_size

        # if start is still less than the length of results, do one more copy
        if block_start < len(tup_set):
            # split values
            val_list = tup_set[block_start:len(tup_set)]

            copy = IteratorFile((commands.format(*vals) for vals in val_list))

            cur.copy_from(copy, 'temp_tbl')

        cur.close()
        # persist changes
        conn.commit()

    except Exception as e:
        print("An exception occurred while trying to create a cursor: ", e)
    finally:
        if conn is not None:
            conn.close()

    print("copy done")

    new_res = connection.execute(select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.dofd, temp_tbl.c.compare_date, temp_tbl.c.prior_dofd, temp_tbl.c.prior_acct_stat).where(
        and_(
            base.c.cons_acct_num == temp_tbl.c.prior_acct_num,
            base.c.file == header.c.file,
            base.c.dofd != temp_tbl.c.prior_dofd,
            func.to_date(header.c.date_created, date_format) == func.to_date(temp_tbl.c.compare_date, date_format),
            base.c.acct_stat.in_(['61', '62', '63', '64', '65', '71', '78', '80', '82', '83', '84', '93', '94', '95', '96', '97'])
        )
    ))

    print("second query done")

    new_res_set = list()

    for result in new_res:
        new_res_set.append(result)

    return new_res_set

eval_prog_dofd_1 = Evaluator(
    "PROG-DOFD-1",
    "This period's date of first delinquency does not match the previous period when both periods had delinquent account statuses.",
    ['database record id', 'date created', 'consumer account number', 'account status', 'date of first delinquency', 'previous date created', 'previous date of first delinquency', 'previous account status'],
    longitudinal_func = eval_prog_dofd_1_func
)

def eval_prog_status_1_func(connection):
    res = connection.execute(select(header.c.date_created, base.c.cons_acct_num, base.c.acct_stat).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat == '71'
        )
    ))
    res_set = list()
    
    for prev_date_created, acct_num, prev_acct_stat in res:
        compare_date = datetime.strptime(prev_date_created, strptime_format) + relativedelta(months=+1)
        compare_date_str = compare_date.strftime(strptime_format)
        new_res = connection.execute(select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, literal(prev_date_created), literal(prev_acct_stat)).where(
            and_(
                base.c.cons_acct_num == acct_num,
                base.c.file == header.c.file,
                func.to_date(header.c.date_created, date_format) == func.to_date(compare_date_str, date_format),
                base.c.acct_stat.in_(['80', '82', '83', '84'])
            )
        ))
        
        for result in new_res:
            res_set.append(result)

    return res_set

eval_prog_status_1 = Evaluator(
    "PROG-STATUS-1",
    "Prior Account Status indicates that the account was 30-59 days past due, but this month's account status suggests the account is 90 or more days past due.",
    ['database record id', 'date created', 'consumer account number', 'account status', 'previous date created', 'previous account status'],
    longitudinal_func=eval_prog_status_1_func
)

eval_addl_apd_1 = Evaluator(
    "ADDL-APD-1",
    "The account status indicates a delinquent account, but there is no amount past due.",
    ['database record id', 'date created', 'consumer account number', 'account status', 'amount past due'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat.in_(['71', '78', '80', '82', '83', '84', '93', '97']),
            cast(base.c.amt_past_due, Integer) == 0
        )
    ))
)

eval_addl_doai_1 = Evaluator(
    "ADDL-DOAI-1",
    "A paid or settled account status indicated but date of account information is not equal to the date of last payment.",
    ['database record id', 'date created', 'consumer account number', 'account status', 'date of account information', 'date of last payment'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.doai, base.c.dolp).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat.in_(['13', '61', '62', '63', '64', '65']),
            base.c.doai != base.c.dolp
        )
    ))
)

eval_13_10B_1 = Evaluator(
    "13-10B-1",
    "Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the base segment. But there is no date of first delinquency",
    ['database record id', 'date created', 'consumer account number', 'account status', 'amount past due', 'base consumer information indicator', 'current balance', 'date closed', 'date of first delinquency', 'scheduled monthly payment amount'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due, base.c.cons_info_ind, base.c.current_bal, base.c.date_closed, base.c.dofd, base.c.smpa).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat == '97',
            base.c.cons_info_ind.in_(['E', 'F', ' E', ' F', 'E ', 'F ']),
            base.c.dofd.in_(['00000000','        ', ''])
        )
    ))
)

eval_13_10B_2 = Evaluator(
    "13-10B-2",
    "Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the J1 segment. But there is no date of first delinquency",
    ['database record id', 'date created', 'consumer account number', 'account status', 'amount past due', 'J1 consumer information indicator', 'current balance', 'date closed', 'date of first delinquency', 'scheduled monthly payment amount'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due, j1.c.cons_info_ind_j1, base.c.current_bal, base.c.date_closed, base.c.dofd, base.c.smpa).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == j1.c.id,
            base.c.acct_stat == '97',
            j1.c.cons_info_ind_j1.in_(['E', 'F', ' E', ' F', 'E ', 'F ']),
            base.c.dofd.in_(['00000000','        ', ''])
        )
    ))
)

eval_13_10B_3 = Evaluator(
    "13-10B-3",
    "Account indicates a discharge for Chapter 7 or 11 bankruptcy for a charged off obligation in the J2 segment. But there is no date of first delinquency",
    ['database record id', 'date created', 'consumer account number', 'account status', 'amount past due', 'J2 consumer information indicator', 'current balance', 'date closed', 'date of first delinquency', 'scheduled monthly payment amount'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due, j2.c.cons_info_ind_j2, base.c.current_bal, base.c.date_closed, base.c.dofd, base.c.smpa).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == j2.c.id,
            base.c.acct_stat == '97',
            j2.c.cons_info_ind_j2.in_(['E', 'F', ' E', ' F', 'E ', 'F ']),
            base.c.dofd.in_(['00000000','        ', ''])
        )
    ))
)

eval_7_21C_1 = Evaluator(
    "7-21C-1",
    "Special comment code suggests that the account was paid in full for less than the full balance, but the account status does not indicate the account was paid.",
    ['database record id',
    'date created',
    'consumer account number',
    'account status',
    'amount past due',
    'current balance',
    'date closed',
    'special comment code'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due, base.c.current_bal, base.c.date_closed, base.c.spc_com_cd).where(
        and_(
            base.c.file == header.c.file,
            ~base.c.acct_stat.in_(['13', '61', '62', '63', '64', '65']),
            base.c.spc_com_cd == 'AU'
        )
    ))
)

eval_7_21C_2 = Evaluator(
    "7-21C-2",
    "Special comment code suggests that the account was paid in full for less than the full balance, but the account status does not indicate the account was paid. Includes a K2 segment.",
    ['database record id',
    'date created',
    'consumer account number',
    'account status',
    'amount past due',
    'current balance',
    'date closed',
    'special comment code',
    'K2 purchased - sold indicator',
    'K2 purchased - sold name'],
    func = lambda: (select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.amt_past_due, base.c.current_bal, base.c.date_closed, base.c.spc_com_cd, k2.c.k2_purch_sold_ind, k2.c.k2_purch_sold_name).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == k2.c.id,
            ~base.c.acct_stat.in_(['13', '61', '62', '63', '64', '65']),
            base.c.spc_com_cd == 'AU'
        )
    ))
)

def eval_9_4A_1_func(connection):
    res = connection.execute(select(header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, base.c.cons_info_ind).where(
        and_(
            base.c.file == header.c.file,
            base.c.acct_stat == '71',
            base.c.cons_info_ind.in_(['', '  '])
        )
    ))
    res_set = list()
    
    for prev_date_created, acct_num, prev_acct_stat, prev_cons_info_ind in res:
        compare_date = datetime.strptime(prev_date_created, strptime_format) + relativedelta(months=+1)
        compare_date_str = compare_date.strftime(strptime_format)
        new_res = connection.execute(select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.php, literal(prev_date_created), literal(prev_acct_stat), literal(prev_cons_info_ind)).where(
            and_(
                base.c.cons_acct_num == acct_num,
                base.c.file == header.c.file,
                func.to_date(header.c.date_created, date_format) == func.to_date(compare_date_str, date_format),
                ~base.c.php.startswith('1')
            )
        ))
        
        for result in new_res:
            res_set.append(result)

    return res_set

eval_9_4A_1 = Evaluator(
    "9-4A-1",
    "When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the base segment.",
    ['database record id',
    'date created',
    'consumer account number',
    'payment history profile (first character)',
    'previous date created',
    'previous account status',
    'previous consumer information indicator (base segment)'],
    longitudinal_func=eval_9_4A_1_func
)

def eval_9_4A_2_func(connection):
    res = connection.execute(select(header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, j1.c.cons_info_ind_j1).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == j1.c.id,
            base.c.acct_stat == '71',
            j1.c.cons_info_ind_j1.in_(['', '  '])
        )
    ))
    res_set = list()
    
    for prev_date_created, acct_num, prev_acct_stat, prev_cons_info_ind_j1 in res:
        compare_date = datetime.strptime(prev_date_created, strptime_format) + relativedelta(months=+1)
        compare_date_str = compare_date.strftime(strptime_format)
        new_res = connection.execute(select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.php, literal(prev_date_created), literal(prev_acct_stat), literal(prev_cons_info_ind_j1)).where(
            and_(
                base.c.cons_acct_num == acct_num,
                base.c.file == header.c.file,
                func.to_date(header.c.date_created, date_format) == func.to_date(compare_date_str, date_format),
                ~base.c.php.startswith('1')
            )
        ))
        
        for result in new_res:
            res_set.append(result)

    return res_set

eval_9_4A_2 = Evaluator(
    "9-4A-2",
    "When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the J1 segment.",
    ['database record id',
    'date created',
    'consumer account number',
    'payment history profile (first character)',
    'previous date created',
    'previous account status',
    'previous consumer information indicator (J1 segment)'],
    longitudinal_func=eval_9_4A_2_func
)

def eval_9_4A_3_func(connection):
    res = connection.execute(select(header.c.date_created, base.c.cons_acct_num, base.c.acct_stat, j2.c.cons_info_ind_j2).where(
        and_(
            base.c.file == header.c.file,
            base.c.id == j2.c.id,
            base.c.acct_stat == '71',
            j2.c.cons_info_ind_j2.in_(['', '  '])
        )
    ))
    res_set = list()
    
    for prev_date_created, acct_num, prev_acct_stat, prev_cons_info_ind_j2 in res:
        compare_date = datetime.strptime(prev_date_created, strptime_format) + relativedelta(months=+1)
        compare_date_str = compare_date.strftime(strptime_format)
        new_res = connection.execute(select(base.c.id, header.c.date_created, base.c.cons_acct_num, base.c.php, literal(prev_date_created), literal(prev_acct_stat), literal(prev_cons_info_ind_j2)).where(
            and_(
                base.c.cons_acct_num == acct_num,
                base.c.file == header.c.file,
                func.to_date(header.c.date_created, date_format) == func.to_date(compare_date_str, date_format),
                ~base.c.php.startswith('1')
            )
        ))
        
        for result in new_res:
            res_set.append(result)

    return res_set

eval_9_4A_3 = Evaluator(
    "9-4A-3",
    "When the account status for the previous period reported the account 30-59 days past due, the first entry of this payment history profile is not '1' which would imply that the previous period's account was 30-59 days past due. Consumer info indicator is blank in the J2 segment.",
    ['database record id',
    'date created',
    'consumer account number',
    'payment history profile (first character)',
    'previous date created',
    'previous account status',
    'previous consumer information indicator (J1 segment)'],
    longitudinal_func=eval_9_4A_3_func
)

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
    # eval_addl_apd_1,
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
