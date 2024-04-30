from datetime import date, timedelta
from evaluate_m2.evaluate import evaluator

from parse_m2.models import (
    AccountActivity, AccountHolder, J1,
    J2, K2, K4, L1, M2DataFile, Metro2Event
)
import calendar


def get_prior_months_by_number(activity_date: date, month_cnt=1):
    """
    Given a date activity_date, calculate the total days of the month and return the previous month.

    Inputs:
    `activity_date` - the date to be compared
    `month_cnt` - the number of months
    """
    prev_date:date
    total_days = 0

    if month_cnt > 1:
        m = activity_date.month
        y = activity_date.year
        for i in range(0, month_cnt):
            # Get the days in the provided month
            days_in_month = calendar.monthrange(y, m)[1]
            total_days += days_in_month
            if m == 1:
                m = 12
                y -= 1
            else:
                m -= i
        prev_date=activity_date - timedelta(days=total_days)
    else:
        days_in_month = calendar.monthrange(activity_date.year, activity_date.month)[1]
        prev_date=activity_date - timedelta(days=days_in_month)

    return prev_date

def acct_record(file: M2DataFile, custom_values: dict):
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
        # AccountHolder values
        "cons_info_ind": "",
        # Shared values (used in both AccountHolder and AccountActivity)
        "activity_date": date(2022, 5, 30),
        "cons_acct_num": "",
        # AccountActivity values
        "id":"1",
        "port_type": "A",
        "acct_type": "",
        "date_open": date(2018, 2, 28),
        "credit_limit": 0,
        "hcola": 0,
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
    }
    # Override defaults with provided values
    values = default_values | custom_values
    # Create the AccountHolder record with provided values
    acct_holder = AccountHolder(
        data_file = file,
        activity_date=values["activity_date"],
        cons_acct_num = values["cons_acct_num"],
        cons_info_ind = values["cons_info_ind"],
    )
    acct_holder.save()
    # Create the AccountActivity record with provided values
    acct_activity = AccountActivity(
        id=values["id"],
        account_holder=acct_holder,
        activity_date=values["activity_date"],
        cons_acct_num = values["cons_acct_num"],
        port_type = values["port_type"],
        acct_type = values["acct_type"],
        date_open = values["date_open"],
        credit_limit = values["credit_limit"],
        hcola = values["hcola"],
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
    return acct_activity

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
        'change_ind': '1',
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
    activity_date=date(2019, 12, 31)
    evaluators = evaluator.evaluators

    def create_bulk_account_holders(self, file: M2DataFile, cons_info_ind_list: tuple):
        # Create bulk account holder data
        account_holders=[]
        for i in range(0, len(cons_info_ind_list)):
            account_holders.append(
                self.create_acct_holder(file, cons_info_ind_list[i])
            )
        return AccountHolder.objects.bulk_create(account_holders)

    def create_bulk_activities(self, data_file: M2DataFile, value_list: dict, size: int):
        account_activities=[]

        for i in range(0, size):
            account_activities.append(self.create_acct_activity(
                id=value_list['id'][i]
                    if "id" in value_list else 1,
                account_holder=AccountHolder.objects.get(
                        cons_info_ind=value_list['account_holder'][i])
                    if "account_holder" in value_list
                    else AccountHolder.objects.get(
                        id=value_list['account_holder_id'][i].id)
                    if "account_holder_id" in value_list
                    else self.create_acct_holder(data_file),
                acct_stat=value_list['acct_stat'][i]
                    if "acct_stat" in value_list else '00',
                acct_type=value_list['acct_type'][i]
                    if "acct_type" in value_list else '00',
                activity_date=value_list['activity_date']
                    if "activity_date" in value_list else date(2019, 12, 31),
                actual_pmt_amt=value_list['actual_pmt_amt'][i]
                    if "actual_pmt_amt" in value_list else 0,
                amt_past_due=value_list['amt_past_due'][i]
                    if "amt_past_due" in value_list else 0,
                cons_acct_num=value_list['cons_acct_num'][i]
                    if "cons_acct_num" in value_list else '012345',
                compl_cond_cd=value_list['compl_cond_cd'][i]
                    if "compl_cond_cd" in value_list else '0',
                credit_limit=value_list['credit_limit'][i]
                    if "credit_limit" in value_list else 0,
                current_bal=value_list['current_bal'][i]
                    if "current_bal" in value_list else 0,
                date_closed=value_list['date_closed'][i]
                    if "date_closed" in value_list else date(2020, 1, 1),
                date_open=value_list['date_open'][i]
                    if "date_open" in value_list else date(2020, 1, 1),
                doai=value_list['doai'][i]
                    if "doai" in value_list else date(2020, 1, 1),
                dofd=value_list['dofd'][i]
                    if "dofd" in value_list else date(2020, 1, 1),
                hcola=value_list['hcola'][i]
                    if "hcola" in value_list else 0,
                orig_chg_off_amt=value_list['orig_chg_off_amt'][i]
                    if "orig_chg_off_amt" in value_list else 0,
                php=value_list['php'][i]
                    if "php" in value_list else 'X',
                port_type=value_list['port_type'][i]
                    if "port_type" in value_list else 'X',
                pmt_rating=value_list['pmt_rating'][i]
                    if "pmt_rating" in value_list else '0',
                smpa=value_list['smpa'][i]
                    if "smpa" in value_list else 0,
                spc_com_cd=value_list['spc_com_cd'][i]
                    if "spc_com_cd" in value_list else 'X',
                terms_dur=value_list['terms_dur'][i]
                    if "terms_dur" in value_list else '0',
                terms_freq=value_list['terms_freq'][i]
                    if "terms_freq" in value_list else '0'
                ))
        return AccountActivity.objects.bulk_create(account_activities)

    def create_bulk_JSegments(self, j_type: str, value_list: dict, size: int):
        # Create bulk account holder data
        j_segments=[]
        if size > 1:
            for i in range(0, size):
                j_segments.append(
                    self.create_jsegment(
                        id=value_list['account_activity'][i],
                        j_type=j_type,
                        cons_info_ind=value_list['cons_info_ind'][i])
                )
        else:
            j_segments.append(
                self.create_jsegment(
                    id=value_list['account_activity'],
                    j_type=j_type,
                    cons_info_ind=value_list['cons_info_ind'])
            )
        if j_type == 'j1':
            return J1.objects.bulk_create(j_segments)
        else:
            return J2.objects.bulk_create(j_segments)

    def create_acct_holder(self, file: M2DataFile, cons_info_ind='X'):
        return AccountHolder(data_file=file, activity_date=self.activity_date,
            surname='Doe', first_name='Jane', middle_name='A', gen_code='F',
            ssn='012345678', dob='01012000', phone_num='0123456789', ecoa='0',
            cons_info_ind=cons_info_ind, cons_acct_num='012345')

    def create_acct_activity(self, id: int, account_holder: AccountHolder,
        acct_stat: str, acct_type: str, activity_date: date, actual_pmt_amt: int,
        amt_past_due: int, cons_acct_num: int, compl_cond_cd: int, credit_limit: int,
        current_bal: int, date_closed: date, date_open: date, doai: date,
        dofd: date, hcola: int, orig_chg_off_amt: int, php:str, pmt_rating: str,
        port_type: str, smpa: int, spc_com_cd: str, terms_dur: str, terms_freq: str,):

        return AccountActivity(
            id=id, account_holder=account_holder, acct_stat=acct_stat,
            acct_type=acct_type, activity_date=activity_date,
            actual_pmt_amt=actual_pmt_amt, amt_past_due=amt_past_due,
            cons_acct_num=cons_acct_num, compl_cond_cd=compl_cond_cd,
            credit_limit=credit_limit, current_bal=current_bal,
            date_closed=date_closed, date_open=date_open, doai=doai,
            dofd=dofd, hcola=hcola, orig_chg_off_amt=orig_chg_off_amt,
            php=php, pmt_rating=pmt_rating, port_type=port_type, smpa=smpa,
            spc_com_cd=spc_com_cd, terms_dur=terms_dur, terms_freq=terms_freq)

    def create_jsegment(self, id: int, j_type: str, cons_info_ind: str):
        if j_type == 'j1':
            return  J1(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)
        else:
            return  J2(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)

    def create_k2(self, id: int, purch_sold_ind: str, purch_sold_name: str):
        return  K2(account_activity=AccountActivity.objects.get(id=id),
                   purch_sold_ind=purch_sold_ind, purch_sold_name=purch_sold_name)

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
                output = func(record_set)
                results = sorted(output, key=lambda x: x['id'])
                expected = sorted(expected_result, key=lambda x: x['id'])
                # print('-'*50, '\n', eval_name, '\n', '-'*50,)
                # print('\nRESULTS: ', results, '\n')
                # print('\nEXPECTED: ', expected, '\n\n')
        # Exactly one evaluator should have run
        self.assertEqual(evaluators_matching, 1)

        # compare expected result with actual result
        self.assertEqual(expected, results)
