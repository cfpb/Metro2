from datetime import datetime

from evaluate_m2.m2_evaluators.addl_dofd_evals import evaluators as addl_dofd_evals
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals
from evaluate_m2.m2_evaluators.cat7_evals import evaluators as cat7_evals
from parse_m2.models import (
    AccountActivity, AccountHolder, J1,
    J2, K2, L1, M2DataFile, Metro2Event
)

class EvaluatorTestHelper():
    activity_date=datetime(2019, 12, 31)
    date=datetime(2020, 1, 1)
    evaluators = addl_dofd_evals + cat7_evals + cat12_evals

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
                    else self.create_acct_holder(data_file),
                acct_stat=value_list['acct_stat'][i]
                    if "acct_stat" in value_list else '00',
                acct_type=value_list['acct_type'][i]
                    if "acct_type" in value_list else '00',
                activity_date=value_list['activity_date'][i]
                    if "activity_date" in value_list else datetime(2019, 12, 31),
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
                    if "date_closed" in value_list else datetime(2020, 1, 1),
                date_open=value_list['date_open'][i]
                    if "date_open" in value_list else datetime(2020, 1, 1),
                doai=value_list['doai'][i]
                    if "doai" in value_list else datetime(2020, 1, 1),
                dofd=value_list['dofd'][i]
                    if "dofd" in value_list else datetime(2020, 1, 1),
                hcola=value_list['hcola'][i]
                    if "hcola" in value_list else 0,
                orig_chg_off_amt=value_list['orig_chg_off_amt'][i]
                    if "orig_chg_off_amt" in value_list else 0,
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

    def create_bulk_k2(self, value_list: dict, size):
        k2_list=[]

        for i in range(0, size):
            k2_list.append(self.create_k2(
                id=value_list['id'][i]
                    if "id" in value_list else 1,
                purch_sold_ind=value_list['purch_sold_ind'][i]
                    if "purch_sold_ind" in value_list else '1',
                purch_sold_name=value_list['purch_sold_name'][i]
                    if "purch_sold_name" in value_list else 'Bank Bank',
            ))
        return K2.objects.bulk_create(k2_list)


    def create_acct_holder(self, file: M2DataFile, cons_info_ind='X'):
        return AccountHolder(data_file=file, activity_date=self.activity_date,
            surname='Doe', first_name='Jane', middle_name='A', gen_code='F',
            ssn='012345678', dob='01012000', phone_num='0123456789', ecoa='0',
            cons_info_ind=cons_info_ind)

    def create_acct_activity(self, id: int, account_holder: AccountHolder,
        acct_stat: str, acct_type: str, activity_date: datetime, actual_pmt_amt: int,
        amt_past_due: int, cons_acct_num: int, compl_cond_cd: int, credit_limit: int,
        current_bal: int, date_closed: datetime, date_open: datetime, doai: datetime,
        dofd: datetime, hcola: int, orig_chg_off_amt: int, pmt_rating: str,
        port_type: str, smpa: int, spc_com_cd: str, terms_dur: str, terms_freq: str,):

        return AccountActivity(
            id=id, account_holder=account_holder, acct_stat=acct_stat,
            acct_type=acct_type, activity_date=activity_date,
            actual_pmt_amt=actual_pmt_amt, amt_past_due=amt_past_due,
            cons_acct_num=cons_acct_num, compl_cond_cd=compl_cond_cd,
            credit_limit=credit_limit, current_bal=current_bal,
            date_closed=date_closed, date_open=date_open, doai=doai,
            dofd=dofd, hcola=hcola, orig_chg_off_amt=orig_chg_off_amt,
            pmt_rating=pmt_rating, port_type=port_type, smpa=smpa,
            spc_com_cd=spc_com_cd, terms_dur=terms_dur, terms_freq=terms_freq)

    def create_jsegment(self, id: int, j_type: str, cons_info_ind: str):
        if j_type == 'j1':
            return  J1(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)
        else:
            return  J2(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)

    def create_k2(self, id: int, purch_sold_ind: str, purch_sold_name: str):
        return  K2(account_activity=AccountActivity.objects.get(id=id), purch_sold_ind=purch_sold_ind,
                   purch_sold_name=purch_sold_name)


    def create_l1(self, id=1, change_ind='1', new_acc_num='9876543210',
                  new_id_num='1234567890'):
        return  L1(account_activity=AccountActivity.objects.get(id=id),
                   change_ind=change_ind, new_acc_num=new_acc_num, new_id_num=new_id_num)

    def assert_evaluator_correct(self, event: Metro2Event, eval_name: str, expected_result: list[dict]):
        # Test that the evaluator:
        # 1. Name matches an evaluator in evaluators.py
        # 2. Is included in the list of evaluators to run
        # 3. Produces results in the expected format
        # 4. Triggers on the correct record
        evaluators_matching = 0
        record_set = event.get_all_account_activity()
        for eval in self.evaluators:
            if eval.name == eval_name:
                evaluators_matching += 1
                output = eval.func(record_set)
                results = sorted(list(output), key=lambda x: x['id'])
                expected = sorted(expected_result, key=lambda x: x['id'])
                # print('\n\nRESULTS: ', results, '\n\n')
                # print('\n\nEXPECTED: ', expected, '\n\n')
        # Exactly one evaluator should have run
        self.assertEqual(evaluators_matching, 1)

        # compare expected result with actual result
        self.assertEqual(expected, results)
