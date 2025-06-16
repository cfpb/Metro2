// M2 fields mapped to their human-readable names
// Ordered according to their position in M2 reporting,
// with base segment values first.
// This order is used in the account view tables.
const M2_FIELD_NAMES = new Map([
  ['activity_date', 'Activity date'],
  ['id_num', 'ID number'],
  ['cons_acct_num', 'Account number'],
  ['port_type', 'Portfolio type'],
  ['acct_type', 'Account type'],
  ['date_open', 'Date opened'],
  ['credit_limit', 'Credit limit'],
  ['hcola', 'HCOLA'],
  ['terms_dur', 'Terms duration'],
  ['terms_freq', 'Terms frequency'],
  ['smpa', 'Scheduled monthly payment amount'],
  ['actual_pmt_amt', 'Actual payment amount'],
  ['acct_stat', 'Account status'],
  ['pmt_rating', 'Payment rating'],
  ['php', 'Payment history profile'],
  ['php1', 'Payment history profile (most recent entry)'],
  ['spc_com_cd', 'Special comment code'],
  ['compl_cond_cd', 'Compliance condition code'],
  ['current_bal', 'Current balance'],
  ['amt_past_due', 'Amount past due'],
  ['orig_chg_off_amt', 'Original charge-off amount'],
  ['doai', 'Date of account information'],
  ['dofd', 'DOFD'],
  ['date_closed', 'Date closed'],
  ['dolp', 'Date of last payment'],
  ['int_type_ind', 'Interest type indicator'],
  ['account_holder__first_name', 'Account holder first name'],
  ['account_holder__surname', 'Account holder surname'],
  [
    'account_holder__cons_info_ind',
    'Bankruptcy - Consumer information indicator for account holder'
  ],
  ['account_holder__ecoa', 'ECOA code for account holder'],
  [
    'account_holder__cons_info_ind_assoc',
    'Bankruptcy - Consumer information indicator for associated consumers'
  ],
  ['account_holder__ecoa_assoc', 'ECOA codes for associated consumers'],
  ['k2__purch_sold_ind', 'Purchased-sold indicator (K2)'],
  ['k2__purch_sold_name', 'Purchased-sold name (K2)'],
  ['k4__balloon_pmt_amt', 'Balloon payment amount (K4)'],
  ['l1__change_ind', 'Account change indicator (L1)'],
  ['l1__new_acc_num', 'New consumer account number (L1)'],
  ['l1__new_id_num', 'New identification number (L1)'],
  ['previous_values__account_holder__first_name', 'Prior account holder first name'],
  ['previous_values__account_holder__surname', 'Prior account holder surname'],
  ['previous_values__activity_date', 'Prior activity date'],
  ['previous_values__id_num', 'Prior ID number'],
  ['previous_values__port_type', 'Prior portfolio type'],
  ['previous_values__acct_type', 'Prior account type'],
  ['previous_values__date_open', 'Prior date open'],
  ['previous_values__acct_stat', 'Prior account status'],
  ['previous_values__pmt_rating', 'Prior payment rating'],
  ['previous_values__current_bal', 'Prior current balance'],
  ['previous_values__orig_chg_off_amt', 'Prior original charge-off amount'],
  ['previous_values__dofd', 'Prior DOFD'],
  ['previous_values__date_closed', 'Prior date closed'],
  [
    'previous_values__account_holder__cons_info_ind',
    'Prior bankruptcy - Consumer information indicator for account holder'
  ],
  [
    'previous_values__account_holder__cons_info_ind_assoc',
    'Prior bankruptcy - Consumer information indicator for associated consumers'
  ],
  ['previous_values__account_holder__ecoa', 'Prior ECOA code for account holder'],
  ['previous_values__l1__change_ind', 'Prior account change indicator (L1)'],
  ['previous_values__l1__new_acc_num', 'Prior new consumer account number (L1)'],
  ['previous_values__l1__new_id_num', 'Prior new identification number (L1)']
])

export default M2_FIELD_NAMES
