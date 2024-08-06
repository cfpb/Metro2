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
}

# Invert the dict above to map the other direction
plain_to_code_field_map = {v.lower(): k for k, v in code_to_plain_field_map.items()}


fields_used_format = """
Identifying information
DB record id
activity date
consumer account number

Fields used for evaluator
used_fields

Helpful fields that are also displayed currently
display_fields
"""
def format_fields_used_for_csv(fields_used: list, fields_display: list):
    return fields_used_format \
        .replace('used_fields', '\n'.join(fields_used)) \
        .replace('display_fields', '\n'.join(fields_display))

def parse_fields_used_from_csv(input: str):
    """
    In the source of truth spreadsheet, the 'fields used' column
    is a newline-delimited string with section headers to indicate
    which fields are 'fields_used' vs 'fields_display'. Get the
    appropriate items and return them as a list.
    """
    input_list = input.lower().splitlines()
    # Remove leading and trailing whitespaces in each item in list
    input_list = [x.strip() for x in input_list]
    header = 'fields used for evaluator'
    try:
        start = input_list.index(header)
        try:
            end = input_list[start:].index('')
            # Return all items between the header and the next blank line
            items = input_list[start+1:start+end]
        except ValueError:
            # If no blank line after header, return all items after header
            items = input_list[start+1:]
    except ValueError:
        # If the header isn't present, return all items
        items = input_list

    # Filter out blank lines
    return list(filter(len, items))

def parse_fields_display_from_csv(input: str):
    input_list = input.lower().splitlines()
    # Remove leading and trailing whitespaces in each item in list
    input_list = [x.strip() for x in input_list]
    header = 'helpful fields that are also displayed currently'
    try:
        start = input_list.index(header)
        # Return all items after the header
        items = input_list[start+1:]
    except ValueError:
        # If the header isn't present, do not return any item
        items = []

    # Filter out blank lines
    return list(filter(len, items))
