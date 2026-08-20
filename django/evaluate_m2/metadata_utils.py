valid_fields = [
    # Account Activity fields
    "id",
    "cons_acct_num",
    "activity_date",
    "port_type",
    "acct_type",
    "date_open",
    "credit_limit",
    "hcola",
    "terms_dur",
    "terms_freq",
    "smpa",
    "actual_pmt_amt",
    "acct_stat",
    "pmt_rating",
    "php",
    "spc_com_cd",
    "compl_cond_cd",
    "current_bal",
    "amt_past_due",
    "orig_chg_off_amt",
    "doai",
    "dofd",
    "date_closed",
    "dolp",
    "id_num",

    # Account Holder fields
    "ecoa",
    "cons_info_ind",
    "cons_info_ind_assoc",
    "ecoa_assoc",
    "first_name",
    "surname",

    # K segments
    "k2__purch_sold_ind",
    "k2__purch_sold_name",
    "k4__balloon_pmt_amt",

    # L segment
    "l1__change_ind",
    "l1__new_acc_num",
    "l1__new_id_num",

    # Prior record fields
    "previous_values__activity_date",
    "previous_values__port_type",
    "previous_values__acct_type",
    "previous_values__date_open",
    "previous_values__acct_stat",
    "previous_values__pmt_rating",
    "previous_values__current_bal",
    "previous_values__orig_chg_off_amt",
    "previous_values__dofd",
    "previous_values__date_closed",
    "previous_values__id_num",

    "previous_values__cons_info_ind",
    "previous_values__cons_info_ind_assoc",
    "previous_values__ecoa",
    "previous_values__first_name",
    "previous_values__surname",

    "previous_values__l1__change_ind",
    "previous_values__l1__new_acc_num",
    "previous_values__l1__new_id_num",
]

def format_fields_for_csv(fields: list) -> str:
    return ';'.join(fields)

def parse_fields_from_csv(input: str) -> list[str]:
    """
    In the source of truth spreadsheet, the 'fields used' and
    'fields supplement' columns come in as semicolon-delimited
    strings. Return the list of items.
    """
    if input.strip():
        return [val.strip() for val in input.split(";")]
    else:
        return []
