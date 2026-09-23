# Map the column names in the EvaluatorResultMaterializedView
# to their human-friendly names, for use in CSV downloads
# of evaluator results

# Where possible, these names match the names in
# /front-end/src/constants/m2FieldNames.ts
M2_FIELD_NAMES = {
    # Account activity fields
    'activity_date': 'Activity date',
    'cons_acct_num': 'Account number',
    'id_num': 'ID number',
    'port_type': 'Portfolio type',
    'acct_type': 'Account type',
    'date_open': 'Date opened',
    'credit_limit': 'Credit limit',
    'hcola': 'HCOLA',
    'terms_dur': 'Terms duration',
    'terms_freq': 'Terms frequency',
    'smpa': 'Scheduled monthly payment amount',
    'actual_pmt_amt': 'Actual payment amount',
    'acct_stat': 'Account status',
    'pmt_rating': 'Payment rating',
    'php1': 'Payment history profile',
    'php': 'Payment history profile (all entries)',
    'spc_com_cd': 'Special comment code',
    'compl_cond_cd': 'Compliance condition code',
    'current_bal': 'Current balance',
    'amt_past_due': 'Amount past due',
    'orig_chg_off_amt': 'Original charge-off amount',
    'doai': 'Date of account information',
    'dofd': 'DOFD',
    'date_closed': 'Date closed',
    'dolp': 'Date of last payment',
    'int_type_ind': 'Interest type indicator',

    # Account holder fields
    'first_name': 'Account holder first name',
    'middle_name': 'Account holder middle name',
    'surname': 'Account holder surname',
    'gen_code': 'Generation code',
    'ssn': 'Social security number',
    'dob': 'Date of birth',
    'phone_num': 'Telephone number',
    'cons_info_ind': 'Consumer information indicator',
    'ecoa': 'ECOA code for account holder',
    'cons_info_ind_assoc': 'Consumer information indicator - J1+J2 segments',
    'ecoa_assoc': 'ECOA codes for associated consumers',
    'addr_line_1': 'Address (line 1)',
    'addr_line_2': 'Address (line 2)',
    'city': 'City',
    'state': 'State',
    'zip': 'ZIP/postal code',
    'addr_ind': 'Address indicator',
    'res_cd': 'Residence code',

    # Extra segment fields
    'purch_sold_ind': 'Purchased-sold indicator (K2)',
    'purch_sold_name': 'Purchased-sold name (K2)',
    'spc_pmt_ind': 'Specialized payment indicator (K4)',
    'balloon_pmt_amt': 'Balloon payment amount (K4)',
    'deferred_pmt_st_dt': 'Deferred payment start date (K4)',
    'balloon_pmt_due_dt': 'Balloon payment due date (K4)',
    'change_ind': 'Account change indicator (L1)',
    'new_acc_num': 'New consumer account number (L1)',
    'new_id_num': 'New identification number (L1)',

    # Previous values fields
    'prior_first_name': 'Prior account holder first name',
    'prior_surname': 'Prior account holder surname',
    'prior_activity_date': 'Prior activity date',
    'prior_id_num': 'Prior ID number',
    'prior_port_type': 'Prior portfolio type',
    'prior_acct_type': 'Prior account type',
    'prior_date_open': 'Prior date open',
    'prior_acct_stat': 'Prior account status',
    'prior_pmt_rating': 'Prior payment rating',
    'prior_current_bal': 'Prior current balance',
    'prior_orig_chg_off_amt': 'Prior original charge-off amount',
    'prior_dofd': 'Prior DOFD',
    'prior_date_closed': 'Prior date closed',
    'prior_cons_info_ind': 'Prior bankruptcy - Consumer information indicator for account holder',  # noqa: E501
    'prior_cons_info_ind_assoc': 'Prior bankruptcy - Consumer information indicator for associated consumers',  # noqa: E501
    'prior_ecoa': 'Prior ECOA code for account holder',
    'prior_ecoa_assoc': 'Prior ECOA codes for associated consumers',
    'prior_change_ind': 'Prior account change indicator (L1)',
    'prior_new_acc_num': 'Prior new consumer account number (L1)',
    'prior_new_id_num': 'Prior new identification number (L1)'
}
