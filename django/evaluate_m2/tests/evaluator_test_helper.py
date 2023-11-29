from datetime import datetime
from evaluate_m2.m2_evaluators.cat12_evals import evaluators as cat12_evals
from parse_m2.models import AccountActivity, AccountHolder, J1, J2, K2, L1, M2DataFile

class EvaluatorTestHelper():
    activity_date=datetime(2019, 12, 31)
    date=datetime(2020, 1, 1)
    evaluators = cat12_evals

    def create_bulk_account_holders(self, file: M2DataFile, cons_info_ind_list: tuple):
        # Create bulk account holder data
        account_holders=[]
        for i in range(0, len(cons_info_ind_list)):
            account_holders.append(
                self.create_acct_holder(file, cons_info_ind_list[i])
            )
        return AccountHolder.objects.bulk_create(account_holders)

    def create_bulk_activities(self, value_list: dict, size: int):
        account_activities=[]

        for i in range(0, size):
            account_activities.append(self.create_acct_activity(
                id=self.get_field_value(value_list['id']
                    if "id" in value_list else (), i, 1),
                account_holder=self.get_account_holder(value_list['account_holder'], i),
                acct_stat=self.get_field_value( value_list['acct_stat']
                    if "acct_stat" in value_list else (), i, '00'),
                acct_type=self.get_field_value(value_list['acct_type']
                    if "acct_type" in value_list else (), i, '00'),
                amt_past_due=self.get_field_value(value_list['amt_past_due']
                    if "amt_past_due" in value_list else (), i, 0),
                cons_acct_num=self.get_field_value(value_list['cons_acct_num']
                    if "cons_acct_num" in value_list else (), i, '012345'),
                credit_limit=self.get_field_value(value_list['credit_limit']
                    if "credit_limit" in value_list else (), i, 0),
                current_bal=self.get_field_value(value_list['current_bal']
                    if "current_bal" in value_list else (), i, 0),
                dofd=self.get_field_value(value_list['dofd']
                    if "dofd" in value_list else (), i, datetime(2020, 1, 1)),
                hcola=self.get_field_value(value_list['hcola']
                    if "hcola" in value_list else (), i, 0),
                port_type=self.get_field_value(value_list['port_type']
                    if "port_type" in value_list else (), i, 'X'),
                pmt_rating=self.get_field_value(value_list['pmt_rating']
                    if "pmt_rating" in value_list else (), i, '0'),
                spc_com_cd=self.get_field_value(value_list['spc_com_cd']
                    if "spc_com_cd" in value_list else (), i, 'X'),
                terms_dur=self.get_field_value(value_list['terms_dur']
                    if "terms_dur" in value_list else (), i, '0'),
                terms_freq=self.get_field_value(value_list['terms_freq']
                    if "terms_freq" in value_list else (), i, '0')
                ))
        return AccountActivity.objects.bulk_create(account_activities)

    def create_acct_holder(self, file: M2DataFile, cons_info_ind='X'):
        return AccountHolder(data_file=file, activity_date=self.activity_date,
            surname='Doe', first_name='Jane', middle_name='A', gen_code='F',
            ssn='012345678', dob='01012000', phone_num='0123456789', ecoa='0',
            cons_info_ind=cons_info_ind)

    def create_acct_activity(self, id: int, account_holder: AccountHolder,
        acct_stat: str, acct_type: str, amt_past_due: int, cons_acct_num: int, credit_limit: int, current_bal: int, hcola: int, port_type: str,
        spc_com_cd: str, terms_dur: str, terms_freq: str, dofd: datetime,
        pmt_rating: str, actual_pmt_amt=0, orig_chg_off_amt=0, smpa=0):
        return AccountActivity(
            id=id, account_holder=account_holder, acct_stat=acct_stat, acct_type=acct_type, activity_date=self.activity_date, amt_past_due=amt_past_due, actual_pmt_amt=actual_pmt_amt, cons_acct_num=cons_acct_num, credit_limit=credit_limit, current_bal=current_bal, date_closed=self.date, date_open=self.date, doai=self.date, hcola=hcola, orig_chg_off_amt=orig_chg_off_amt, port_type=port_type, smpa=smpa, spc_com_cd=spc_com_cd, terms_dur=terms_dur, terms_freq=terms_freq, dofd=dofd, pmt_rating=pmt_rating)

    def create_jsegment(self, id: int, j_type: str, cons_info_ind: str):
        if j_type == 'j1':
            return  J1(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)
        else:
            return  J2(account_activity=AccountActivity.objects.get(id=id), cons_info_ind=cons_info_ind)

    def create_k2(self, id: int, purch_sold_ind: str, purch_sold_name: str):
        return  K2(account_activity=AccountActivity.objects.get(id=id), purch_sold_ind=purch_sold_ind, purch_sold_name=purch_sold_name)

    def get_account_holder(self, data: str, index: int):
        if (len(data) > 1):
            return AccountHolder.objects.get(cons_info_ind=data[index])
        else:
            return AccountHolder.objects.get(cons_info_ind=data[0])

    def get_field_value(self, data: tuple, index: str, default):
        if data:
            return data[index]
        else:
            return default

    def create_l1(self, id=1, change_ind='1', new_acc_num='9876543210', new_id_num='1234567890'):
        return  L1(account_activity=AccountActivity.objects.get(id=id), change_ind=change_ind, new_acc_num=new_acc_num, new_id_num=new_id_num)

    def assert_evaluator_correct(self, eval_name: str, expected_result: list[dict]):
        # Test that the evaluator:
        # 1. Name matches an evaluator in evaluators.py
        # 2. Is included in the list of evaluators to run
        # 3. Produces results in the expected format
        # 4. Triggers on the correct record
        evaluators_matching = 0
        for eval in self.evaluators:
            if eval.name == eval_name:
                # This is left for debugging purposes to view the query
                # print('\n\n', eval.func.query)
                evaluators_matching += 1
                output = eval.func
                results = sorted(list(output), key=lambda x: x['id'])
                expected = sorted(expected_result, key=lambda x: x['id'])
                # print('\n\nRESULTS: ', results, '\n\n')
                # print('\n\nEXPECTED: ', expected, '\n\n')
        # Exactly one evaluator should have run
        self.assertEqual(evaluators_matching, 1)

        # compare expected result with actual result
        self.assertEqual(expected, results)
