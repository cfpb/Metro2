// M2 fields that can be displayed for an account record
export interface AccountRecord {
  activity_date?: string | null
  id_num?: string | null
  cons_acct_num?: string | null
  port_type?: string | null
  acct_type?: string | null
  date_open?: string | null
  credit_limit?: number | null
  hcola?: number | null
  terms_dur?: string | null
  terms_freq?: string | null
  smpa?: number | null
  actual_pmt_amt?: number | null
  acct_stat?: string | null
  pmt_rating?: string | null
  php?: string | null
  php1?: string | null
  spc_com_cd?: string | null
  compl_cond_cd?: string | null
  current_bal?: number | null
  amt_past_due?: number | null
  orig_chg_off_amt?: number | null
  doai?: string | null
  dofd?: string | null
  date_closed?: string | null
  dolp?: string | null
  account_holder__cons_info_ind?: string | null
  account_holder__ecoa?: string | null
  account_holder__cons_info_ind_assoc?: string[] | null
  account_holder__ecoa_assoc?: [] | null
  k2__purch_sold_ind?: string | null
  k2__purch_sold_name?: string | null
  k4__balloon_pmt_amt?: string | null
  l1__change_ind?: string | null
  l1__new_acc_num?: string | null
  l1__new_id_num?: string | null
  previous_values__account_holder__cons_info_ind?: string | null
  previous_values__account_holder__cons_info_ind_assoc?: [] | null
  previous_values__account_holder__ecoa?: string | null
  previous_values__account_holder__first_name?: string | null
  previous_values__account_holder__surname?: string | null
  previous_values__l1__change_ind?: string | null
  previous_values__l1__new_acc_num?: string | null
  previous_values__l1__new_id_num?: string | null
  previous_values__activity_date?: string | null
  previous_values__port_type?: string | null
  previous_values__acct_type?: string | null
  previous_values__date_open?: string | null
  previous_values__acct_stat?: string | null
  previous_values__pmt_rating?: string | null
  previous_values__current_bal?: number | null
  previous_values__orig_chg_off_amt?: number | null
  previous_values__dofd?: string | null
  previous_values__date_closed?: string | null
  previous_values__id_num?: string | null
}

// M2 fields mapped to their human-readable names
// Ordered according to their position in M2 reporting,
// with base segment values first.
// This order is used in the account view tables.
export const M2_FIELD_NAMES = new Map([
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
  // ['account_holder__surname', ''],
  // ['account_holder__first_name', ''],
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
  [
    'previous_values__account_holder__cons_info_ind',
    'Prior consumer information indicator for account holder'
  ],
  [
    'previous_values__account_holder__cons_info_ind_assoc',
    'Prior consumer information indicators for associated consumers'
  ],
  ['previous_values__account_holder__ecoa', 'Prior ECOA code for account holder'],
  ['previous_values__account_holder__first_name', 'Prior first name'],
  ['previous_values__account_holder__surname', 'Prior surname'],
  ['previous_values__l1__change_ind', 'Prior account change indicator (L1)'],
  ['previous_values__l1__new_acc_num', 'Prior new consumer account number (L1)'],
  ['previous_values__l1__new_id_num', 'Prior new identification number (L1)'],
  ['previous_values__activity_date', 'Prior activity date'],
  ['previous_values__port_type', 'Prior portfolio type'],
  ['previous_values__acct_type', 'Prior account type'],
  ['previous_values__date_open', 'Prior date open'],
  ['previous_values__acct_stat', 'Prior account status'],
  ['previous_values__pmt_rating', 'Prior payment rating'],
  ['previous_values__current_bal', 'Prior current balance'],
  ['previous_values__orig_chg_off_amt', 'Prior original charge-off amount'],
  ['previous_values__dofd', 'Prior date of first delinquency'],
  ['previous_values__date_closed', 'Prior date closed'],
  ['previous_values__id_num', 'Prior ID number']
])

export const COL_DEF_CONSTANTS = {
  activity_date: { type: 'formattedDate', minWidth: 160 },
  actual_pmt_amt: { type: 'currency' },
  amt_past_due: { type: 'currency' },
  credit_limit: { type: 'currency' },
  current_bal: { type: 'currency' },
  date_open: { type: 'formattedDate', minWidth: 100 },
  date_closed: { type: 'formattedDate', minWidth: 110 },
  doai: { type: 'formattedDate', minWidth: 155 },
  dofd: { type: 'formattedDate', minWidth: 100 },
  dolp: { type: 'formattedDate', minWidth: 120 },
  hcola: { type: 'currency' },
  php: { minWidth: 265 },
  php1: { minWidth: 220 },
  orig_chg_off_amt: { type: 'currency' },
  smpa: { type: 'currency', minWidth: 140 },
  account_holder__cons_info_ind: { minWidth: 265 },
  account_holder__cons_info_ind_assoc: { minWidth: 265 },
  account_holder__ecoa: { minWidth: 230 },
  account_holder__ecoa_assoc: { minWidth: 230 },
  k2__purch_sold_ind: { minWidth: 250 },
  k2__purch_sold_name: { minWidth: 210 },
  k4__balloon_pmt_amt: { type: 'currency' },
  l1__change_ind: { minWidth: 200 },
  l1__new_acc_num: { minWidth: 200 },
  l1__new_id_num: { minWidth: 200 },
  previous_values__account_holder__cons_info_ind: { minWidth: 265 },
  previous_values__account_holder__cons_info_ind_assoc: { minWidth: 265 },
  previous_values__account_holder__ecoa: { minWidth: 230 },
  previous_values__l1__change_ind: { minWidth: 200 },
  previous_values__l1__new_acc_num: { minWidth: 200 },
  previous_values__l1__new_id_num: { minWidth: 200 },
  previous_values__activity_date: { type: 'formattedDate', minWidth: 160 },
  previous_values__date_open: { type: 'formattedDate', minWidth: 100 },
  previous_values__dofd: { type: 'formattedDate', minWidth: 100 },
  previous_values__date_closed: { type: 'formattedDate', minWidth: 110 },
  previous_values__current_bal: { type: 'currency' },
  previous_values__orig_chg_off_amt: { type: 'currency' }
}

// Lookup to use evaluator id segments as initial categorization
export const evaluatorSegmentMap = new Map([
  ['status', 'Account status'],
  ['type', 'Account type'],
  ['paymentamount', 'Actual payment amount'],
  ['apd', 'Amount past due'],
  ['balloon', 'Balloon payment amount'],
  ['bankruptcy', 'Bankruptcy'],
  ['chargeoff', 'Original charge-off amount'],
  ['creditlimit', 'Credit limit'],
  ['balance', 'Current balance'],
  ['ccc', 'Compliance condition code'],
  ['dateclosed', 'Date closed'],
  ['dateopen', 'Date open'],
  ['deferred', 'Deferred'],
  ['doai', 'Date of account information'],
  ['dofd', 'Date of first delinquency'],
  ['dolp', 'Date of last payment'],
  ['ecoa', 'ECOA (equal credit opportunity act)'],
  ['hcola', 'HCOLA (highest credit or original loan amount)'],
  ['id', 'Account ID number'],
  ['j1j2', 'J1 or J2 associated consumer'],
  ['number', 'Account number'],
  ['purchasedsold', 'K2 purchased-sold indicator'],
  ['php', 'Payment history profile'],
  ['rating', 'Payment rating'],
  ['portfolio', 'Portfolio type'],
  ['prog', 'Progression'],
  ['smpa', 'Scheduled monthly payment amount'],
  ['scc', 'Special comment code'],
  ['termsduration', 'Terms duration'],
  ['accountchange', 'L1 change indicator']
])

export const PII_COOKIE_NAME = 'acceptedPIIWarning'
