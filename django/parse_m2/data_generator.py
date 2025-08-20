import random

from datetime import datetime, date, timedelta

from parse_m2 import fields
from parse_m2.models import (
    AccountActivity, AccountHolder, J1, J2, K4
)


def save_m2_file(filename: str, size: int, activity_date: date):
    with open(filename, mode='w+') as f:
        f.write(header_segment_data(activity_date) + "\n")
        for x in range(size):
            # A random-looking acct num that gets used once in every generated file
            acct_num = 123456789 + (13783 * x)
            write_one_row(f, activity_date, acct_num)

def write_one_row(f, activity_date: date, acct_num: int) -> str:
    # Write base segment
    acct_activity = generate_acct_activity(activity_date, acct_num)
    acct_holder = generate_acct_holder(acct_num)
    f.write(base_segment_data(acct_activity, acct_holder))

    # Write some extra segments
    for segment_type in pick_extra_segments():
        if segment_type == 'J1':
            f.write(j1_segment_data(generate_j1()))
        elif segment_type == 'J2':
            f.write(j2_segment_data(generate_j2()))
        elif segment_type == 'K4':
            f.write(k4_segment_data(generate_k4()))

    # End with a newline
    f.write("\n")

available_extra_segments = [None, 'J1', 'J2', 'K4']
segment_weights = [70, 10, 10, 10]

def pick_extra_segments():
    # Choose up to two extra segments for sample data
    picks = random.choices(available_extra_segments, segment_weights, k=2)
    # can't have more than one K4
    if picks == ['K4', 'K4']:
        picks = ['K4']
    return picks

#######################################
## Methods for generating fake account data
#######################################
def generate_acct_activity(activity_date: date, acct_num: int) -> AccountActivity:
    credit_limit = random.randrange(1000,99000)
    acct_stat = random.choice(acct_statuses)

    return AccountActivity(
        activity_date = activity_date, # acct nums are usually formatted like numbers
        cons_acct_num = format_num_value(acct_num, 30),
        id_num = 'FURNISHER ID',
        port_type = 'C',  # Line of credit
        acct_type = random.choice(acct_types),
        date_open = random_date(date(2000,1,1), date(2010,1,1)),  # accts opened in the oughts
        credit_limit = credit_limit,  # credit limits btw 1k and 100k
        hcola = random.randrange(credit_limit),  # highest credit used is a num less than credit_limit
        terms_dur = "LOC",  # Port type "C" always uses "LOC"
        terms_freq = "M",  # Assume monthly billing
        smpa = 100,  # unsure
        actual_pmt_amt = random.randrange(int(credit_limit/20)),  # pay up to 5% of credit limit per cycle
        acct_stat = acct_stat,  # any acct status
        pmt_rating = pmt_rating_pick(acct_stat),  # pick a pmt rating only if acct_stat indicates it should be present
        php = '',  # TODO
        spc_com_cd = random.choice(spc_com_cds),
        compl_cond_cd = random.choice(compl_cond_cds),
        current_bal = random.randrange(credit_limit + int(credit_limit*0.1)),  # can be higher than credit limit
        amt_past_due = '',  # TODO
        orig_chg_off_amt = ocoa_pick(acct_stat, credit_limit),
        doai = activity_date,
        dofd = dofd_pick(acct_stat),  # a date after date_open, or None
        date_closed = None,  # assuming not closed (for now)
        dolp = random_date(activity_date - timedelta(days=90), activity_date),  # a date in the 3 months before activity_date
        int_type_ind = 'F',  # fixed interest
    )

def generate_acct_holder(acct_num: int) -> AccountHolder:
    return AccountHolder(
        # Person-related fields
        cons_info_ind = random.choices(cons_info_inds, weights=cii_weights, k=1)[0],
        first_name = 'FIRSTNAME',
        middle_name = 'MIDDLENAME',
        surname = f'SURNAME{acct_num}',
        dob = '12311990',
        phone_num = '5558675309',
        ssn = '333224444',
        ecoa = random.choice(ecoa_codes),

        # Address-related fields
        country_cd = 'US',
        addr_line_1 = 'ADDR LINE 1',
        addr_line_2 = 'ADDR LINE 2',
        city = 'WASHINGTON',
        state = 'DC',
        zip = '20002',
        addr_ind = '',
        res_cd = '',
    )

def generate_j1() -> J1:
    return J1(
        cons_info_ind = random.choices(cons_info_inds, weights=cii_weights, k=1)[0],
        first_name = 'FIRSTNAME J1',
        middle_name = 'MIDDLENAME J1',
        surname = 'SURNAME J1',
        dob = '12311977',
        phone_num = '4448675309',
        ssn = '333225555',
        ecoa = random.choice(ecoa_codes),
    )

def generate_j2() -> J2:
    return J2(
        cons_info_ind = random.choices(cons_info_inds, weights=cii_weights, k=1)[0],
        first_name = 'FIRSTNAME J2',
        middle_name = 'MIDDLENAME J2',
        surname = 'SURNAME J2',
        dob = '12311977',
        phone_num = '4448675309',
        ssn = '333225555',
        ecoa = random.choice(ecoa_codes),

        country_cd = 'US',
        addr_line_1 = 'ADDR1 J2',
        addr_line_2 = 'ADDR2 J2',
        city = 'ARLINGTON',
        state = 'VA',
        zip = '22209',
        addr_ind = '',
        res_cd = '',
    )

def generate_k4() -> K4:
    return K4(
        spc_pmt_ind = '01',
        deferred_pmt_st_dt = None,
        balloon_pmt_due_dt = random_date(date(2014,1,1), date(2016,1,1)),
        balloon_pmt_amt = random.randrange(300, 900, 25)
    )

# acct types acceptable for port_type 'C', plus an invalid one to trigger evaluator Portfolio-Type-1
acct_types = ['9A', '7A', '47', '15']

acct_statuses = ['05','11','13','61','62','63','64','65',
                    '71','78','80','82','83','84','88','89',
                    '93','94','95','96','97','DA','DF']

def dofd_pick(acct_stat: str):
    if acct_stat in ['05','11','13', 'DA', 'DF']:
        return None
    else:
        return random_date(date(2010,1,1), date(2016,1,1))

spc_com_cds = [
    'M', 'AP', 'AS', 'AT', 'CI', 'CJ', 'CL',
    'AM', 'S', 'V', 'AV', 'BO', 'CH', 'AI'
]  # selected codes valid for port type "C", not the whole list

compl_cond_cds = ['', 'XA', 'XB', 'XC', 'XD', 'XE', 'XF',
                  'XG', 'XH', 'XJ', 'XR']

def ocoa_pick(acct_stat: str, credit_limit: int):
    if acct_stat in ['64', '97']:
        return random.randrange(int(credit_limit * 0.4))
    else:
        return None

def pmt_rating_pick(acct_stat: str) -> str:
    if acct_stat in ['13', '65', '88', '89', '94', '95']:
        options = [0, 1, 2, 3, 4, 5, 6, 'G', 'L']
        return str(random.choice(options))
    else:
        return ''

ecoa_codes = ['1', '2', '3', '5', '7', 'T', 'X', 'W', 'Z']

cons_info_inds = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                 '1A', 'Q', 'R', 'V', '2A', 'S', 'T', 'U']
cii_weights = [74, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

def random_date(start: date, end: date) -> date:
    span = end - start
    pick = random.randrange(span.days)
    return start + timedelta(pick)

#######################################
## Methods for serializing AccountActivity data
#######################################

def header_segment_data(activity_date: date) -> str:
    # start with a string of 426 meaningless characters
    seg = blank_segment('header')
    # replace the only field that matters (activity date) with data
    seg = set_field_value(fields.header_fields, 'activity_date', activity_date, seg)
    return seg

def base_segment_data(acct_activity: AccountActivity, acct_hldr: AccountHolder):
    # start with a string of 426 meaningless characters
    seg = blank_segment("base")
    bf = fields.base_fields

    # replace individual fields with meaningful data
    # AccountActivity fields
    seg = set_field_value(bf, "cons_acct_num", acct_activity.cons_acct_num, seg)
    seg = set_field_value(bf, "port_type", acct_activity.port_type, seg)
    seg = set_field_value(bf, "acct_type", acct_activity.acct_type, seg)
    seg = set_field_value(bf, "date_open", acct_activity.date_open, seg)
    seg = set_field_value(bf, "credit_limit", acct_activity.credit_limit, seg)
    seg = set_field_value(bf, "hcola", acct_activity.hcola, seg)
    seg = set_field_value(bf, "id_num", acct_activity.id_num, seg)
    seg = set_field_value(bf, "terms_dur", acct_activity.terms_dur, seg)
    seg = set_field_value(bf, "terms_freq", acct_activity.terms_freq, seg)
    seg = set_field_value(bf, "smpa", acct_activity.smpa, seg)
    seg = set_field_value(bf, "actual_pmt_amt", acct_activity.actual_pmt_amt, seg)
    seg = set_field_value(bf, "acct_stat", acct_activity.acct_stat, seg)
    seg = set_field_value(bf, "pmt_rating", acct_activity.pmt_rating, seg)
    seg = set_field_value(bf, "php", acct_activity.php, seg)
    seg = set_field_value(bf, "spc_com_cd", acct_activity.spc_com_cd, seg)
    seg = set_field_value(bf, "compl_cond_cd", acct_activity.compl_cond_cd, seg)
    seg = set_field_value(bf, "current_bal", acct_activity.current_bal, seg)
    seg = set_field_value(bf, "amt_past_due", acct_activity.amt_past_due, seg)
    seg = set_field_value(bf, "orig_chg_off_amt", acct_activity.orig_chg_off_amt, seg)
    seg = set_field_value(bf, "doai", acct_activity.doai, seg)
    seg = set_field_value(bf, "dofd", acct_activity.dofd, seg)
    seg = set_field_value(bf, "date_closed", acct_activity.date_closed, seg)
    seg = set_field_value(bf, "dolp", acct_activity.dolp, seg)
    seg = set_field_value(bf, "int_type_ind", acct_activity.int_type_ind, seg)

    # AccountHolder fields
    seg = set_field_value(bf, "surname", acct_hldr.surname, seg)
    seg = set_field_value(bf, "first_name", acct_hldr.first_name, seg)
    seg = set_field_value(bf, "middle_name", acct_hldr.middle_name, seg)
    seg = set_field_value(bf, "gen_code", acct_hldr.gen_code, seg)
    seg = set_field_value(bf, "ssn", acct_hldr.ssn, seg)
    seg = set_field_value(bf, "dob", acct_hldr.dob, seg)
    seg = set_field_value(bf, "phone_num", acct_hldr.phone_num, seg)
    seg = set_field_value(bf, "ecoa", acct_hldr.ecoa, seg)
    seg = set_field_value(bf, "cons_info_ind", acct_hldr.cons_info_ind, seg)
    seg = set_field_value(bf, "country_cd", acct_hldr.country_cd, seg)
    seg = set_field_value(bf, "addr_line_1", acct_hldr.addr_line_1, seg)
    seg = set_field_value(bf, "addr_line_2", acct_hldr.addr_line_2, seg)
    seg = set_field_value(bf, "city", acct_hldr.city, seg)
    seg = set_field_value(bf, "state", acct_hldr.state, seg)
    seg = set_field_value(bf, "zip", acct_hldr.zip, seg)
    seg = set_field_value(bf, "addr_ind", acct_hldr.addr_ind, seg)
    seg = set_field_value(bf, "res_cd", acct_hldr.res_cd, seg)
    return seg

def j1_segment_data(j1: J1) -> str:
    # start with a string of meaningless characters of the right length
    seg = blank_segment("j1")
    f = fields.j1_fields
    # replace individual fields with meaningful data
    seg = set_field_value(f, "surname_j1", j1.surname, seg)
    seg = set_field_value(f, "first_name_j1", j1.first_name, seg)
    seg = set_field_value(f, "middle_name_j1", j1.middle_name, seg)
    seg = set_field_value(f, "gen_code_j1", j1.gen_code, seg)
    seg = set_field_value(f, "ssn_j1", j1.ssn, seg)
    seg = set_field_value(f, "dob_j1", j1.dob, seg)
    seg = set_field_value(f, "phone_num_j1", j1.phone_num, seg)
    seg = set_field_value(f, "ecoa_j1", j1.ecoa, seg)
    seg = set_field_value(f, "cons_info_ind_j1", j1.cons_info_ind, seg)
    return seg

def j2_segment_data(j2: J2) -> str:
    # start with a string of meaningless characters of the right length
    seg = blank_segment("j2")
    f = fields.j2_fields
    # replace individual fields with meaningful data
    seg = set_field_value(f, "surname_j2", j2.surname, seg)
    seg = set_field_value(f, "first_name_j2", j2.first_name, seg)
    seg = set_field_value(f, "middle_name_j2", j2.middle_name, seg)
    seg = set_field_value(f, "gen_code_j2", j2.gen_code, seg)
    seg = set_field_value(f, "ssn_j2", j2.ssn, seg)
    seg = set_field_value(f, "dob_j2", j2.dob, seg)
    seg = set_field_value(f, "phone_num_j2", j2.phone_num, seg)
    seg = set_field_value(f, "ecoa_j2", j2.ecoa, seg)
    seg = set_field_value(f, "cons_info_ind_j2", j2.cons_info_ind, seg)
    seg = set_field_value(f, "country_cd_j2", j2.country_cd, seg)
    seg = set_field_value(f, "addr_line_1_j2", j2.addr_line_1, seg)
    seg = set_field_value(f, "addr_line_2_j2", j2.addr_line_2, seg)
    seg = set_field_value(f, "city_j2", j2.city, seg)
    seg = set_field_value(f, "state_j2", j2.state, seg)
    seg = set_field_value(f, "zip_j2", j2.zip, seg)
    seg = set_field_value(f, "addr_ind_j2", j2.addr_ind, seg)
    seg = set_field_value(f, "res_cd_j2", j2.res_cd, seg)
    return seg

def k4_segment_data(k4: K4) -> str:
    # start with a string of meaningless characters of the right length
    seg = blank_segment("k4")
    f = fields.k4_fields
    # replace individual fields with meaningful data
    seg = set_field_value(f, "k4_spc_pmt_ind", k4.spc_pmt_ind, seg)
    seg = set_field_value(f, "k4_deferred_pmt_st_dt", k4.deferred_pmt_st_dt, seg)
    seg = set_field_value(f, "k4_balloon_pmt_due_dt", k4.balloon_pmt_due_dt, seg)
    seg = set_field_value(f, "k4_balloon_pmt_amt", k4.balloon_pmt_amt, seg)
    return seg

def blank_segment(segment_type: str) -> str:
    segment_type = segment_type.lower()
    seg_len = fields.seg_length[segment_type]

    if segment_type in ['header', 'trailer']:
        # Segment begins with 4 blank chars, then the segment name
        seg = f"....{segment_type.upper()}"
    else:
        # Each other segment's data starts with the segment type, e.g. "J2"
        seg = f"{segment_type.upper()}"

    # Fill the rest with dots as placeholders
    for _ in range(seg_len - len(seg)):
        seg += "."

    return seg

#######################################
## Helper methods for formatting individual fields
#######################################

def set_field_value(field_ref: dict, field_name: str, input, segment: str):
    field = field_ref[field_name]

    # Unpack the tuple that contains the field info
    try:
        field_start, field_end, field_type = field
    except ValueError:
        field_start, field_end = field
        # default to string if no type is provided
        field_type = "string"

    field_len = field_end - field_start + 1
    value = format_value(input, field_len, field_type)

    # place the field value into the segment at the correct position
    return segment[0:field_start - 1] + value + segment[field_end:]

def format_value(input, field_len: int, field_type: str) -> str:
    if field_type[:4] == "date":
        return format_date_value(input, field_len)
    elif field_type[:7] == "numeric":
        return format_num_value(input, field_len)
    elif field_type == "string":
        return format_str_value(input, field_len)
    else:
        raise Exception("field type error")

def format_date_value(input: datetime, field_len: int) -> str:
    if field_len == 8:
        if input:
            # convert to date format
            return datetime.strftime(input, "%m%d%Y")
        else:
            return "00000000"
    else:
        raise Exception("datetime length error")

def format_num_value(input: int, field_len: int) -> str:
    if not input:
        # if input is None, fill with zeroes
        input = ''
    val = str(input)
    s_len = len(val)
    if field_len >= s_len:
        # right-align and pack with zeroes
        return f"{val:0>{field_len}}"
    else:
        raise Exception("int length error")

def format_str_value(input: str, field_len: int) -> str:
    val = str(input)
    s_len = len(val)
    if field_len > s_len:
        # left-align and pack with spaces
        return f"{val:<{field_len}}"
    else:
        return val[:field_len]
