from sqlalchemy import(
    Column,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

# fixtures for testing

class Cursor():
    def execute(self, *_):
        return [("expected", "sample", "data")]

    def fetchall(self):
        return [("test", "success")]

    def close(self):
        return None

class Connect():
    def cursor(self):
        return Cursor()

    def execute(self, *_):
        return [('a', 'b', 'c', 'd')]

    def close(self):
        return None

Dec_Base = declarative_base()

class Header(Dec_Base):
    __tablename__ = 'header'

    col_id = Column("id", String(24), primary_key=True)
    date_created = Column(String(8))
    file = Column(String(24))
    reporter_name = Column(String(40))

    def __init__(
        self, col_id="hash001", date_created="01012000", file="hash002",
        reporter_name="Test Entity"
    ):
        self.col_id = col_id
        self.date_created = date_created
        self.file = file
        self.reporter_name = reporter_name

    def __repr__(self):
        return (
            "<Header('{self.col_id}', '{self.file}', '{self.date_created}', \
                '{self.reporter_name}')>".format(self=self)
        )

class Base(Dec_Base):
    __tablename__ = 'base'

    col_id = Column("id", String(24), primary_key=True)
    file = Column(String(24))
    proc_ind = Column(String(1))
    id_num = Column(String(20))
    cycle_id = Column(String(2))
    cons_acct_num = Column(String(30))
    port_type = Column(String(1))
    acct_type = Column(String(2))
    date_open = Column(String(8))
    credit_limit = Column(String(9))
    hcola = Column(String(9))
    terms_dur = Column(String(3))
    terms_freq = Column(String(1))
    smpa = Column(String(9))
    actual_pmt_amt = Column(String(9))
    acct_stat = Column(String(2))
    pmt_rating = Column(String(1))
    php = Column(String(24))
    spc_com_cd = Column(String(2))
    compl_cond_cd = Column(String(2))
    current_bal = Column(String(9))
    amt_past_due = Column(String(9))
    orig_chg_off_amt = Column(String(9))
    doai = Column(String(8))
    dofd = Column(String(8))
    date_closed = Column(String(8))
    dolp = Column(String(8))
    int_type_ind = Column(String(1))
    reserved_base_2 = Column(String(17))
    surname = Column(String(25))
    first_name = Column(String(20))
    middle_name = Column(String(20))
    gen_code = Column(String(1))
    ssn = Column(String(9))
    dob = Column(String(8))
    phone_num = Column(String(10))
    ecoa = Column(String(1))
    cons_info_ind = Column(String(2))
    country_cd = Column(String(2))
    addr_line_1 = Column(String(32))
    addr_line_2 = Column(String(32))
    city = Column(String(20))
    state = Column(String(2))
    col_zip = Column("zip", String(9))
    addr_ind = Column(String(1))
    res_cd = Column(String(1))

    def __init__(
        self, col_id="001", file="test.txt", proc_ind="0",
        id_num="1234", cycle_id="00", cons_acct_num="012345",
        port_type="X", acct_type="0", date_open="01012000",
        credit_limit="0", hcola="0", terms_dur="0",
        terms_freq="0", smpa="0", actual_pmt_amt="0",
        acct_stat="00", pmt_rating="0", php="0",
        spc_com_cd="X", compl_cond_cd="X", current_bal="0",
        amt_past_due="0", orig_chg_off_amt="0", doai="01012000",
        dofd="01012000", date_closed="01012000", dolp="01012000",
        int_type_ind="0", reserved_base_2="0", surname="Doe",
        first_name="Jane", middle_name="A", gen_code="0",
        ssn="012345678", dob="01012000", phone_num="0123456789",
        ecoa="0", cons_info_ind="X", country_cd="US",
        addr_line_1="123 Fake St", addr_line_2="Apt 1", city="DC",
        state="MD", col_zip="12345", addr_ind="X",
        res_cd="X"
    ):
        self.col_id = col_id
        self.file = file
        self.proc_ind = proc_ind
        self.id_num = id_num
        self.cycle_id = cycle_id
        self.cons_acct_num = cons_acct_num
        self.port_type = port_type
        self.acct_type = acct_type
        self.date_open = date_open
        self.credit_limit = credit_limit
        self.hcola = hcola
        self.terms_dur = terms_dur
        self.terms_freq = terms_freq
        self.smpa = smpa
        self.actual_pmt_amt = actual_pmt_amt
        self.acct_stat = acct_stat
        self.pmt_rating = pmt_rating
        self.php = php
        self.spc_com_cd = spc_com_cd
        self.compl_cond_cd = compl_cond_cd
        self.current_bal = current_bal
        self.amt_past_due = amt_past_due
        self.orig_chg_off_amt = orig_chg_off_amt
        self.doai = doai
        self.dofd = dofd
        self.date_closed = date_closed
        self.dolp = dolp
        self.int_type_ind = int_type_ind
        self.reserved_base_2 = reserved_base_2
        self.surname = surname
        self.first_name = first_name
        self.middle_name = middle_name
        self.gen_code = gen_code
        self.ssn = ssn
        self.dob = dob
        self.phone_num = phone_num
        self.ecoa = ecoa
        self.cons_info_ind = cons_info_ind
        self.country_cd = country_cd
        self.addr_line_1 = addr_line_1
        self.addr_line_2 = addr_line_2
        self.city = city
        self.state = state
        self.col_zip = col_zip
        self.addr_ind = addr_ind
        self.res_cd = res_cd

    def __repr__(self):
        return (
            "<Header('{self.col_id}', '{self.file}', '{self.proc_ind}', \
                '{self.id_num}', '{self.cycle_id}', '{self.cons_acct_num}', \
                '{self.port_type}', '{self.acct_type}', '{self.date_open}', \
                '{self.credit_limit}', '{self.hcola}', '{self.terms_dur}', \
                '{self.terms_freq}', '{self.smpa}', '{self.actual_pmt_amt}', \
                '{self.acct_stat}', '{self.pmt_rating}', '{self.php}', \
                '{self.spc_com_cd}', '{self.current_bal}', '{self.amt_past_due}', \
                '{self.orig_chg_off_amt}', '{self.doai}', '{self.dofd}', \
                '{self.date_closed}', '{self.dolp}', '{self.int_type_ind}', \
                '{self.reserved_base_2}', '{self.surname}', '{self.first_name}', \
                '{self.middle_name}', '{self.gen_code}', '{self.ssn}', \
                '{self.dob}', '{self.phone_num}', '{self.ecoa}', \
                '{self.cons_info_ind}', '{self.country_cd}', '{self.addr_line_1}', \
                '{self.addr_line_2}', '{self.city}', '{self.state}', \
                '{self.col_zip}', '{self.addr_ind}', '{self.res_cd}', \
                )>".format(self=self)
        )