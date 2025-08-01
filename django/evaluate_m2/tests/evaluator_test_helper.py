from datetime import date
from evaluate_m2.evaluate import evaluator

from parse_m2.models import (
    AccountActivity, AccountHolder, J1,
    J2, K2, K4, L1, M2DataFile, Metro2Event
)


def acct_record(file: M2DataFile, custom_values: dict) -> AccountActivity:
    """
    Returns an AccountActivity record for use in tests, using the values
    provided, or defaulting to basic values where none are provided.
    Also creates the AccountHolder record associated with the AccountActivity
    record.

    Inputs:
    - file: M2DataFile record the AccountHolder record will be associated with
    - custom_values: Dict of values to override the defaults. Keys should match
                     the field names in the AccountActivity and AccountHolder models
    """
    # Set basic defaults for all values in AccountActivity.
    # If we end up needing more values in AccountHolder, add
    # them here as well.
    default_values = {
        # Shared values (used in both AccountHolder and AccountActivity)
        "activity_date": date(2022, 5, 30),
        "cons_acct_num": "",
        # AccountActivity values
        "id":"1",
        "previous_values": None,
        "port_type": "A",
        "acct_type": "",
        "date_open": date(2018, 2, 28),
        "credit_limit": 0,
        "hcola": 0,
        "id_num": "",
        "terms_dur": "00",
        "terms_freq": "00",
        "smpa": 0,
        "actual_pmt_amt": 0,
        "acct_stat": "",
        "pmt_rating": "",
        "php": "",
        "spc_com_cd": "",
        "compl_cond_cd": "",
        "current_bal": 0,
        "amt_past_due": 0,
        "orig_chg_off_amt": 0,
        "doai": date(2022, 5, 1),
        "dofd": None,
        "date_closed": None,
        "dolp": None,
        "int_type_ind": "",

        # AccountHolder values
        "cons_info_ind_assoc": None,
        "ecoa_assoc": None,
        "ecoa": "",
        "cons_info_ind": "",
        "first_name": "",
        "middle_name": "",
        "surname": "",
        "gen_code": "",
        "dob": "",
        "phone_num": "",
        "ssn": "",
    }
    # Override defaults with provided values
    values = default_values | custom_values
    # Create the AccountActivity record with provided values
    acct_activity = AccountActivity(
        id=values["id"],
        data_file = file,
        event=file.event,
        previous_values=values["previous_values"],
        activity_date=values["activity_date"],
        cons_acct_num = values["cons_acct_num"],
        port_type = values["port_type"],
        acct_type = values["acct_type"],
        date_open = values["date_open"],
        credit_limit = values["credit_limit"],
        hcola = values["hcola"],
        id_num = values["id_num"],
        terms_dur = values["terms_dur"],
        terms_freq = values["terms_freq"],
        smpa = values["smpa"],
        actual_pmt_amt = values["actual_pmt_amt"],
        acct_stat = values["acct_stat"],
        pmt_rating = values["pmt_rating"],
        php = values["php"],
        spc_com_cd = values["spc_com_cd"],
        compl_cond_cd = values["compl_cond_cd"],
        current_bal = values["current_bal"],
        amt_past_due = values["amt_past_due"],
        orig_chg_off_amt = values["orig_chg_off_amt"],
        doai = values["doai"],
        dofd = values["dofd"],
        date_closed = values["date_closed"],
        dolp = values["dolp"],
        int_type_ind = values["int_type_ind"],
    )
    acct_activity.save()

    # Create the AccountHolder record with provided values
    acct_holder = AccountHolder(
        id=values["id"],
        account_activity=acct_activity,
        activity_date=values["activity_date"],
        cons_acct_num = values["cons_acct_num"],
        cons_info_ind = values["cons_info_ind"],
        first_name = values["first_name"],
        middle_name = values["middle_name"],
        surname = values["surname"],
        gen_code = values["gen_code"],
        dob = values["dob"],
        phone_num = values["phone_num"],
        ssn = values["ssn"],
        cons_info_ind_assoc = values["cons_info_ind_assoc"],
        ecoa_assoc = values["ecoa_assoc"],
        ecoa = values["ecoa"],
    )
    acct_holder.save()
    return acct_activity

def k2_record(custom_values: dict):
    """
    Returns a K2 record for use in tests, using the values
    provided, or defaulting to basic values where none are provided.
    Inputs:
    - custom_values: Dict of values to override the defaults. Keys should match
                     the field names in the K2 model
    """
    # Set basic defaults for all values in K2.
    default_values = {
        'account_activity': '1',
        'purch_sold_ind': '',
        'purch_sold_name': '',
    }

    # Override defaults with provided values
    values = default_values | custom_values
    k2 = K2(
        account_activity=AccountActivity.objects.get(id=values['id']),
        purch_sold_ind=values['purch_sold_ind'],
        purch_sold_name=values['purch_sold_name']
    )
    k2.save()
    return k2

def k4_record(custom_values: dict):
    """
    Returns a K4 record for use in tests, using the values
    provided, or defaulting to basic values where none are provided.

    Inputs:
    - custom_values: Dict of values to override the defaults. Keys should match
                     the field names in the K4 model
    """
    # Set basic defaults for all values in K4.
    default_values = {
        'account_activity': '1',
        'spc_pmt_ind': '1',
        'deferred_pmt_st_dt': None,
        'balloon_pmt_due_dt': None,
        'balloon_pmt_amt': 0
    }
    # Override defaults with provided values
    values = default_values | custom_values
    k4 = K4(
        account_activity=AccountActivity.objects.get(id=values['id']),
        spc_pmt_ind=values['spc_pmt_ind'],
        deferred_pmt_st_dt=values['deferred_pmt_st_dt'],
        balloon_pmt_due_dt=values['balloon_pmt_due_dt'],
        balloon_pmt_amt=values['balloon_pmt_amt']
    )
    k4.save()
    return k4

def l1_record(custom_values: dict):
    """
    Returns a L1 record for use in tests, using the values
    provided, or defaulting to basic values where none are provided.

    Inputs:
    - custom_values: Dict of values to override the defaults. Keys should match
                     the field names in the L1 model
    """
    # Set basic defaults for all values in L1.
    default_values = {
        'account_activity': '1',
        'change_ind': '',
        'new_acc_num': '',
        'new_id_num': ''
    }
    # Override defaults with provided values
    values = default_values | custom_values
    l1 = L1(
        account_activity=AccountActivity.objects.get(id=values['id']),
        change_ind=values['change_ind'],
        new_acc_num=values['new_acc_num'],
        new_id_num=values['new_id_num']
    )
    l1.save()
    return l1

def create_bulk_acct_record(file: M2DataFile, value_list: dict, size: int):
    """
    Returns a list of AccountActivity records for use in tests, using the values
    provided, or defaulting to basic values where none are provided.
    Also creates the AccountHolder records associated with the AccountActivity
    record.

    Inputs:
    - file: M2DataFile record the AccountHolder records will be associated with
    - value_list: Dict of lists to convert to list of dict to override default_values.
                     Keys should match the field names in the AccountActivity and
                     AccountHolder models
    - size: The number of AccountActivity and AccountHolder records to create
    """
    account_activities:list[AccountActivity] = []
    # Convert dictionary of list to list of dictionaries
    custom_values = [{key : value[i] for key, value in value_list.items()}
        for i in range(size)]

    for i in range(0, size):
        acct_activity = acct_record(file, custom_values[i])
        account_activities.append(acct_activity)
    return account_activities

def create_bulk_JSegments(j_type: str, value_list: dict, size: int):
    """
    Returns a list of J1/J2 records for use in tests, using the values
    provided.

    Inputs:
    - j_type: a string value indicating which J Segment to create.
    - value_list: Dict of lists to convert to list of dict to override default_values.
                     Keys should match the field names in the J Segments
    - size: The number of J Segments to create
    """
    # Create bulk account holder data
    j_segments=[]

    # Convert dictionary of list to list of dictionaries
    custom_values = [{key : value[i] for key, value in value_list.items()}
        for i in range(size)]
    for i in range(0, size):
        values = custom_values[i]
        if j_type == 'j1':
            j_segments.append(J1(
                account_activity=values['account_activity'],
                cons_info_ind=values['cons_info_ind']))
        else:
            j_segments.append(J2(
                account_activity=values['account_activity'],
                cons_info_ind=values['cons_info_ind']))
    if j_type == 'j1':
        return J1.objects.bulk_create(j_segments)
    else:
        return J2.objects.bulk_create(j_segments)


class EvaluatorTestHelper():
    evaluators = evaluator.evaluators

    def assert_evaluator_correct(self, event: Metro2Event, eval_name: str, expected_result: list[dict]):
        # Test that the evaluator:
        # 1. Name matches an evaluator in evaluators.py
        # 2. Is included in the list of evaluators to run
        # 3. Produces results in the expected format
        # 4. Triggers on the correct record
        evaluators_matching = 0
        record_set = event.get_all_account_activity()
        for name, func in self.evaluators.items():
            if name == eval_name:
                # print('\n\n', func(record_set).query)
                evaluators_matching += 1
                output = func(record_set).values('id', 'activity_date', 'cons_acct_num')
                results = sorted(output, key=lambda x: x['id'])
                expected = sorted(expected_result, key=lambda x: x['id'])
                # print('-'*50, '\n', eval_name, '\n', '-'*50,)
                # print('\nRESULTS: ', results, '\n')
                # print('\nEXPECTED: ', expected, '\n\n')
        # Exactly one evaluator should have run
        self.assertEqual(evaluators_matching, 1)

        # compare expected result with actual result
        self.assertEqual(expected, results)
