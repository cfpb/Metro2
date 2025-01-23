# Translate from the plain language field names in the source of
# truth spreadsheet to code names that match the database columns
#
# Any fields that don't appear in the SSOTS are removed.
code_to_plain_field_map = {
    # code : plain language

    # Account Holder fields
    "account_holder__cons_acct_num": "consumer account number",
    "account_holder__ecoa": "ecoa",
    "account_holder__cons_info_ind": "consumer information indicator",
    "account_holder__cons_info_ind_assoc": "consumer information indicators for associated consumers",
    "account_holder__ecoa_assoc": "ECOA for associated consumers",
    "account_holder__first_name": "first name",
    "account_holder__surname": "surname",

    # Account Activity fields
    "activity_date": "activity date",
    "port_type": "portfolio type",
    "acct_type": "account type",
    "date_open": "date open",
    "credit_limit": "credit limit",
    "hcola": "highest credit or loan amount",
    "terms_dur": "terms duration",
    "terms_freq": "terms frequency",
    "smpa": "scheduled monthly payment amount",
    "actual_pmt_amt": "actual payment amount",
    "acct_stat": "account status",
    "pmt_rating": "payment rating",
    "php": "payment history profile",
    "spc_com_cd": "special comment code",
    "compl_cond_cd": "compliance condition code",
    "current_bal": "current balance",
    "amt_past_due": "amount past due",
    "orig_chg_off_amt": "original charge-off amount",
    "doai": "date of account information",
    "dofd": "date of first delinquency",
    "date_closed": "date closed",
    "dolp": "date of last payment",
    "id_num": "ID number",

    # K segments
    "k2__purch_sold_ind": "K2 purchased - sold indicator",
    "k2__purch_sold_name": "K2 purchased - sold name",
    "k4__balloon_pmt_amt": "balloon payment amount",

    # L segment
    "l1__change_ind": "L1 change indicator",
    "l1__new_acc_num": "L1 new account number",
    "l1__new_id_num": "L1 new id number",

    # Prior record fields
    "previous_values__account_holder__cons_info_ind": "prior consumer information indicator",
    "previous_values__account_holder__cons_info_ind_assoc": "prior consumer information indicators for associated consumers",
    "previous_values__account_holder__ecoa": "prior ecoa",
    "previous_values__account_holder__first_name": "prior first name",
    "previous_values__account_holder__surname": "prior surname",

    "previous_values__l1__change_ind": "prior L1 change indicator",
    "previous_values__l1__new_acc_num": "prior L1 new account number",
    "previous_values__l1__new_id_num": "prior L1 new id number",

    "previous_values__activity_date": "prior activity date",
    "previous_values__port_type": "prior portfolio type",
    "previous_values__acct_type": "prior account type",
    "previous_values__date_open": "prior date open",
    "previous_values__acct_stat": "prior account status",
    "previous_values__pmt_rating": "prior payment rating",
    "previous_values__current_bal": "prior current balance",
    "previous_values__orig_chg_off_amt": "prior original charge-off amount",
    "previous_values__dofd": "prior date of first delinquency",
    "previous_values__date_closed": "prior date closed",
    "previous_values__id_num": "prior ID number",
}

# Invert the dict above to map the other direction
plain_to_code_field_map = {v.lower(): k for k, v in code_to_plain_field_map.items()}

def format_fields_for_csv(fields: list):
    return '\n'.join(fields)

def parse_fields_from_csv(input: str):
    """
    In the source of truth spreadsheet, the 'fields used' and 'fields supplement'
    columns come in as newline-delimited strings. Parse the lines and return
    the items.
    """
    input_list = input.lower().splitlines()
    # Remove leading and trailing whitespaces in each item in list
    input_list = [x.strip() for x in input_list]
    # Filter out blank lines
    return list(filter(len, input_list))
