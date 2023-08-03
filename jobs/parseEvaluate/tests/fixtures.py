from sqlalchemy import(
    Column,
    ForeignKey,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# fixtures for testing

class Engine():
    def __init__(self, connect_return=None):
        self.connect_return = connect_return

    def connect(self, creator=None):
        return self.connect_return

    def dispose(self):
        return

class Connection():
    def execute(self, *_):
        return

class Evaluator():
    def __init__(self, custom_func_return=None,
        name="my_eval", description="Test evaluator", fields=None
    ):
        self.custom_func_return = custom_func_return
        self.name = name
        self.description = description
        self.fields = fields

    def exec_custom_func(self, connection, engine):
        return self.custom_func_return

Dec_Base = declarative_base()

class Header(Dec_Base):
    __tablename__ = 'header'

    col_id = Column("id", String(24), primary_key=True)
    date_created = Column(String(8))
    file = Column(String(24), unique=True)
    reporter_name = Column(String(40))

    base = relationship('Base', backref='header', uselist=False)

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
    file = Column(String(24), ForeignKey("header.file"))
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

    # Relationships
    j1 = relationship('J1', back_populates='base')
    j2 = relationship('J2', back_populates='base')
    k2 = relationship('K2', back_populates='base')
    l1 = relationship('L1', back_populates='base')

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
            "<Base('{self.col_id}', '{self.file}', '{self.proc_ind}', \
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

class J1(Dec_Base):
    __tablename__ = 'j1'

    col_id = Column('id', String(24), ForeignKey("base.id"), primary_key=True)
    file = Column(String(24), ForeignKey("header.file"))
    segment_identifier_j1 = Column(String(2))
    reserved_j1 = Column(String(1))
    surname_j1 = Column(String(25))
    first_name_j1 = Column(String(20))
    middle_name_j1 = Column(String(20))
    gen_code_j1 = Column(String(1))
    ssn_j1 = Column(String(9))
    dob_j1 = Column(String(8))
    phone_num_j1 = Column(String(10))
    ecoa_j1 = Column(String(1))
    cons_info_ind_j1 = Column(String(2))
    reserved_j1_2 = Column(String(1))

    # Relationship
    base = relationship("Base", back_populates="j1")

    def __init__(
        self,
        col_id="0001",
        file="file_hash",
        segment_identifier_j1="J1",
        reserved_j1="0",
        surname_j1="Doe",
        first_name_j1="Jane",
        middle_name_j1="A",
        gen_code_j1="0",
        ssn_j1="012345678",
        dob_j1="01012000",
        phone_num_j1="0123456789",
        ecoa_j1="0",
        cons_info_ind_j1="X",
        reserved_j1_2="1"

    ):
        self.col_id = col_id,
        self.file = file,
        self.segment_identifier_j1 = segment_identifier_j1,
        self.reserved_j1 = reserved_j1,
        self.surname_j1 = surname_j1,
        self.first_name_j1 = first_name_j1,
        self.middle_name_j1 = middle_name_j1,
        self.gen_code_j1 = gen_code_j1,
        self.ssn_j1 = ssn_j1,
        self.dob_j1 = dob_j1,
        self.phone_num_j1 = phone_num_j1,
        self.ecoa_j1 = ecoa_j1,
        self.cons_info_ind_j1 = cons_info_ind_j1,
        self.reserved_j1_2 = reserved_j1_2

    def __repr__(self):
        return (
            "<J1('{self.col_id}', '{self.file}', '{self.segment_identifier_j1}', \
                '{self.reserved_j1}', '{self.surname_j1}', '{self.first_name_j1}', \
                '{self.middle_name_j1}', '{self.gen_code_j1}', '{self.ssn_j1}', \
                '{self.dob_j1}', '{self.phone_num_j1}', '{self.ecoa_j1}', \
                '{self.cons_info_ind_j1}', '{self.reserved_j1_2}', \
                )>".format(self=self)
        )

class J2(Dec_Base):
    __tablename__ = 'j2'

    col_id = Column('id', String(24), ForeignKey("base.id"), primary_key=True)
    file = Column(String(24), ForeignKey("header.file"))
    segment_identifier_j2 = Column(String(2))
    reserved_j2 = Column(String(1))
    surname_j2 = Column(String(25))
    first_name_j2 = Column(String(20))
    middle_name_j2 = Column(String(20))
    gen_code_j2 = Column(String(1))
    ssn_j2 = Column(String(9))
    dob_j2 = Column(String(8))
    phone_num_j2 = Column(String(10))
    ecoa_j2 = Column(String(1))
    cons_info_ind_j2 = Column(String(2))
    country_cd_j2 = Column(String(2))
    addr_line_1_j2 = Column(String(32))
    addr_line_2_j2 = Column(String(32))
    city_j2 = Column(String(20))
    state_j2 = Column(String(2))
    col_zip_j2 = Column("zip", String(9))
    addr_ind_j2 = Column(String(1))
    res_cd_j2 = Column(String(1))
    reserved_j2_2 = Column(String(2))

    # Relationship
    base = relationship("Base", back_populates="j2")

    def __init__(
        self, col_id="0001", file="file_hash",
        segment_identifier_j2="J2", reserved_j2="0",
        surname_j2="Doe", first_name_j2="Jane",
        middle_name_j2="A", gen_code_j2="0", ssn_j2="012345678",
        dob_j2="01012000", phone_num_j2="0123456789", ecoa_j2="0",
        cons_info_ind_j2="X", country_cd_j2="US",
        addr_line_1_j2="123 Fake St", addr_line_2_j2="Apt 1",
        city_j2="DC", state_j2="MD", col_zip_j2="12345",
        addr_ind_j2="X", res_cd_j2="X", reserved_j2_2="2"
    ):
        self.col_id = col_id,
        self.file = file,
        self.segment_identifier_j2 = segment_identifier_j2,
        self.reserved_j2 = reserved_j2,
        self.surname_j2 = surname_j2,
        self.first_name_j2 = first_name_j2,
        self.middle_name_j2 = middle_name_j2,
        self.gen_code_j2 = gen_code_j2,
        self.ssn_j2 = ssn_j2,
        self.dob_j2 = dob_j2,
        self.phone_num_j2 = phone_num_j2,
        self.ecoa_j2 = ecoa_j2,
        self.cons_info_ind_j2 = cons_info_ind_j2,
        self.country_cd_j2 = country_cd_j2
        self.addr_line_1_j2 = addr_line_1_j2
        self.addr_line_2_j2 = addr_line_2_j2
        self.city_j2 = city_j2
        self.state_j2 = state_j2
        self.col_zip_j2 = col_zip_j2
        self.addr_ind_j2 = addr_ind_j2
        self.res_cd_j2 = res_cd_j2
        self.reserved_j2_2 = reserved_j2_2

    def __repr__(self):
        return (
            "<J2('{self.col_id}', '{self.file}', '{self.segment_identifier_j2}', \
                '{self.reserved_j2}', '{self.surname_j2}', '{self.first_name_j2}', \
                '{self.middle_name_j2}', '{self.gen_code_j2}', '{self.ssn_j2}', \
                '{self.dob_j2}', '{self.phone_num_j2}', '{self.ecoa_j2}', \
                '{self.cons_info_ind_j2}', '{self.country_cd_j2}', \
                '{self.addr_line_1_j2}', '{self.addr_line_2_j2}', '{self.city_j2}', \
                '{self.state_j2}', '{self.col_zip_j2}', '{self.addr_ind_j2}', \
                '{self.res_cd_j2}', '{self.reserved_j2_2}', \
                )>".format(self=self)
        )

class K2(Dec_Base):
    __tablename__ = 'k2'

    col_id = Column('id', String(24), ForeignKey("base.id"), primary_key=True)
    file = Column(String(24), ForeignKey("header.file"))
    k2_seg_id = Column(String(2))
    k2_purch_sold_ind = Column(String(1))
    k2_purch_sold_name = Column(String(30))
    reserved_k2 = Column(String(1))

    # Relationship
    base = relationship("Base", back_populates="k2")

    def __init__(
        self,
        col_id="0001",
        file="file_hash",
        k2_seg_id="K2",
        k2_purch_sold_ind="1",
        k2_purch_sold_name="Bank Bank",
        reserved_k2="0",
    ):
        self.col_id = col_id
        self.file = file
        self.k2_seg_id = k2_seg_id
        self.k2_purch_sold_ind = k2_purch_sold_ind
        self.k2_purch_sold_name = k2_purch_sold_name
        self.reserved_k2 = reserved_k2

    def __repr__(self):
        return (
            "<K2('{self.col_id}', '{self.file}', '{self.k2_seg_id}', \
                '{self.k2_purch_sold_ind}', '{self.k2_purch_sold_name}', \
                '{self.reserved_k2}', \
                )>".format(self=self)
        )

class L1(Dec_Base):
    __tablename__ = 'l1'

    col_id = Column('id', String(24), ForeignKey("base.id"), primary_key=True)
    file = Column(String(24), ForeignKey("header.file"))
    l1_seg_id = Column(String(2))
    l1_change_ind = Column(String(1))
    l1_new_acc_num = Column(String(30))
    l1_new_id_num = Column(String(20))
    reserved_l1 = Column(String(1))

    # Relationship
    base = relationship("Base", back_populates="l1")

    def __init__(
        self,
        col_id="0001",
        file="file_hash",
        l1_seg_id="L1",
        l1_change_ind="1",
        l1_new_acc_num="9876543210",
        l1_new_id_num="1234567890",
        reserved_l1="0",
    ):
        self.col_id = col_id
        self.file = file
        self.l1_seg_id = l1_seg_id
        self.l1_change_ind = l1_change_ind
        self.l1_new_acc_num = l1_new_acc_num
        self.l1_new_id_num = l1_new_id_num
        self.reserved_l1 = reserved_l1

    def __repr__(self):
        return (
            "<L1('{self.col_id}', '{self.file}', '{self.l1_seg_id}', \
                '{self.l1_change_ind}', '{self.l1_new_acc_num}', \
                '{self.l1_new_id_num}', '{self.reserved_l1}', \
                )>".format(self=self)
        )
