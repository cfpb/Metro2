// M2 fields that can be displayed for an account record
export interface AccountRecord {
  cons_acct_num?: string | null
  activity_date?: string | null
  acct_stat?: string | null
  current_bal?: number | null
  amt_past_due?: number | null
  dofd?: string | null
  pmt_rating?: string | null
  php?: string | null
  php1?: string | null
  smpa?: number | null
  actual_pmt_amt?: number | null
  hcola?: number | null
  orig_chg_off_amt?: number | null
  date_open?: string | null
  date_closed?: string | null
  spc_com_cd?: string | null
  compl_cond_cd?: string | null
  doai?: string | null
  dolp?: string | null
  credit_limit?: number | null
  port_type?: string | null
  acct_type?: string | null
  terms_dur?: string | null
  terms_freq?: string | null
  account_holder__cons_info_ind?: string | null
  j1__cons_info_ind?: string | null
  j2__cons_info_ind?: string | null
  k2_purch_sold_ind?: string | null
  k4__balloon_pmt_amt?: number | null
}

// Canonical list of M2 fields for an account record.
// Ordered for display as columns in account record table
export const M2_FIELDS = [
  'activity_date',
  'acct_stat',
  'current_bal',
  'amt_past_due',
  'dofd',
  'pmt_rating',
  'php',
  'php1',
  'smpa',
  'actual_pmt_amt',
  'hcola',
  'orig_chg_off_amt',
  'date_open',
  'date_closed',
  'spc_com_cd',
  'compl_cond_cd',
  'doai',
  'dolp',
  'credit_limit',
  'port_type',
  'acct_type',
  'terms_dur',
  'terms_freq',
  'account_holder__cons_info_ind',
  'j1__cons_info_ind',
  'j2__cons_info_ind',
  'k4__balloon_pmt_amt'
  // 'int_type_ind'
]

// Maps the ids of Metro2 fields to their human-readable names.
export const FIELD_NAMES_LOOKUP = {
  acct_stat: 'Account status',
  acct_type: 'Account type',
  account_holder__cons_info_ind: 'Consumer information indicator',
  activity_date: 'Activity date',
  actual_pmt_amt: 'Actual payment amount',
  amt_past_due: 'Amount past due',
  compl_cond_cd: 'Compliance condition code',
  cons_acct_num: 'Account number',
  credit_limit: 'Credit limit',
  current_bal: 'Current balance',
  date_open: 'Date open',
  date_closed: 'Date closed',
  doai: 'Date of account information',
  dofd: 'DOFD',
  dolp: 'Date of last payment',
  hcola: 'HCOLA',
  j1__cons_info_ind: 'J1 consumer information indicator',
  j2__cons_info_ind: 'J2 consumer information indicator',
  k2_purch_sold_ind: 'K2 purchased-sold indicator',
  k4__balloon_pmt_amt: 'K4 balloon payment amount',
  orig_chg_off_amt: 'Original charge-off amount',
  php: 'Payment history profile',
  php1: 'Payment history profile (Most recent entry)',
  pmt_rating: 'Payment rating',
  port_type: 'Portfolio type',
  spc_com_cd: 'Special comment code',
  smpa: 'Scheduled monthly payment amount',
  terms_dur: 'Terms duration',
  terms_freq: 'Terms frequency'
}

// Maps the ids of Metro2 fields to their data types
// For use in AgGrid column definitions
export const FIELD_TYPES_LOOKUP = {
  acct_stat: 'plainText',
  acct_type: 'plainText',
  account_holder__cons_info_ind: 'plainText',
  activity_date: 'formattedDate',
  actual_pmt_amt: 'currency',
  amt_past_due: 'currency',
  compl_cond_cd: 'plainText',
  cons_acct_num: 'plainText', // TODO: figure out what this should be, if anything
  credit_limit: 'currency',
  current_bal: 'currency',
  date_open: 'formattedDate',
  date_closed: 'formattedDate',
  doai: 'formattedDate',
  dofd: 'formattedDate',
  dolp: 'formattedDate',
  hcola: 'currency',
  j1__cons_info_ind: 'plainText',
  j2__cons_info_ind: 'plainText',
  k2_purch_sold_ind: 'plainText',
  k4__balloon_pmt_amt: 'currency',
  orig_chg_off_amt: 'currency',
  php: 'plainText',
  php1: 'plainText',
  pmt_rating: 'plainText',
  port_type: 'plainText',
  smpa: 'currency',
  spc_com_cd: 'plainText',
  terms_dur: 'plainText', // TODO: figure out what this should be, if anything
  terms_freq: 'plainText'
}

// Many Metro2 fields contain coded data that needs to be translated
// into a more human-readable format for display in the Metro2 tool.
// The following lookups map a field's possible codes to the definitions
// of the codes provided in the Credit Reporting Resource Guide.

export const ACCOUNT_STATUS_LOOKUP = {
  '05': 'Account transferred',
  '11': 'Current account (0-29 days past the due date)',
  '13': 'Paid or closed account/zero balance',
  '61': 'Account paid in full, was a voluntary surrender',
  '62': 'Account paid in full, was a collection account',
  '63': 'Account paid in full, was a repossession',
  '64': 'Account paid in full, was a charge-off',
  '65': 'Account paid in full. A foreclosure was started.',
  '71': 'Account 30-59 days past the due date',
  '78': 'Account 60-89 days past the due date',
  '80': 'Account 90-119 days past the due date',
  '82': 'Account 120-149 days past the due date',
  '83': 'Account 150-179 days past the due date',
  '84': 'Account 180 days or more past the due date',
  '88': 'Claim filed with government for insured portion of balance on a defaulted loan',
  '89': 'Deed received in lieu of foreclosure on a defaulted mortgage; there may be a balance due',
  '93': 'Account assigned to internal or external collections',
  '94': 'Foreclosure completed; there may be a balance due',
  '95': 'Voluntary surrender; there may be a balance due',
  '96': 'Merchandise was repossessed; there may be a balance due',
  '97': 'Unpaid balance reported as a loss (charge-off)',
  DA: 'Delete entire account (for reasons other than fraud)',
  DF: 'Delete entire account due to confirmed fraud (fraud investigation completed)'
}

export const PAYMENT_RATING_LOOKUP = {
  '0': 'Current account (0–29 days past the due date)',
  '1': '30-59 days past the due date',
  '2': '60-89 days past the due date',
  '3': '90-119 days past the due date',
  '4': '120-149 days past the due date',
  '5': '150-179 days past the due date',
  '6': '180 or more days past the due date',
  G: 'Collection',
  L: 'Charge-off'
}

export const PAYMENT_HISTORY_PROFILE_LOOKUP = {
  '0': '0 – 29 days past due date (current account)',
  '1': '30 - 59 days past due date',
  '2': '60 - 89 days past due date',
  '3': '90 - 119 days past due date',
  '4': '120 - 149 days past due date',
  '5': '150 - 179 days past due date',
  '6': '180 or more days past due date',
  B: 'No payment history available prior to this time',
  D: 'No payment history reported/available this month',
  E: 'Zero balance and Account Status 11',
  G: 'Collection',
  H: 'Foreclosure Completed',
  J: 'Voluntary Surrender',
  K: 'Repossession',
  L: 'Charge-off'
}

export const SPECIAL_COMMENT_CODE_LOOKUP = {
  B: 'Account payments managed by financial counseling program.',
  C: 'Paid by Co-maker or Guarantor.',
  H: 'Loan assumed by another party.',
  I: 'Election of Remedy',
  M: 'Account Closed at Credit Grantor’s Request',
  O: 'Account transferred to another company/servicer.',
  S: 'Special handling. Contact credit grantor for additional information.',
  V: 'Adjustment pending.',
  AB: 'Debt being paid through insurance.',
  AC: 'Paying under a partial payment agreement.',
  AH: 'Purchased by another company.',
  AI: 'Recalled to active military duty.',
  AM: 'Account payments assured by wage garnishment.',
  AN: 'Account acquired by FDIC/NCUA.',
  AO: 'Voluntarily surrendered - then redeemed or reinstated.',
  AP: 'Credit Line suspended.',
  AS: 'Account closed due to refinance.',
  AT: 'Account closed due to refinance.',
  AU: 'Account paid in full for less than the full balance',
  AV: 'First payment never received.',
  AW: 'Affected by natural or declared disaster.',
  AX: 'Account paid from collateral.',
  AZ: 'Redeemed or reinstated repossession.',
  BA: 'Transferred to Recovery.',
  BB: 'Full termination/status pending.',
  BC: 'Full termination/obligation satisfied.',
  BD: 'Full termination/balance owing.',
  BE: 'Early termination/status pending.',
  BF: 'Early termination/obligation satisfied.',
  BG: 'Early termination/balance owing.',
  BH: 'Early termination/insurance loss.',
  BI: 'Involuntary repossession.',
  BJ: 'Involuntary repossession/obligation satisfied.',
  BK: 'Involuntary repossession/balance owing.',
  BL: 'Credit card lost or stolen.',
  BN: 'Paid by company which originally sold the merchandise.',
  BO: 'Foreclosure proceedings started.',
  BP: 'Paid through insurance.',
  BS: 'Prepaid lease',
  BT: 'Principal deferred/Interest payment only.',
  CH: 'Guaranteed/Insured.',
  CI: 'Account closed due to inactivity.',
  CJ: 'Credit line no longer available – in repayment phase.',
  CK: 'Credit line reduced due to collateral depreciation.',
  CL: 'Credit line suspended due to collateral depreciation.',
  CM: 'Collateral released by creditor / Balance owing.',
  CN: 'Loan modified under a federal government plan.',
  CO: 'Loan modified.',
  CP: 'Account in forbearance.',
  CS: 'Child support',
  DE: 'Debt extinguished under state law.',
  AL: 'Student Loan Assigned to Government'
}

export const COMPLIANCE_CONDTION_CODE_LOOKUP = {
  XA: 'Account closed at consumer’s request',
  XB: 'Account information has been disputed by the consumer directly to the data furnisher under the Fair Credit Reporting Act (FCRA); the data furnisher is conducting its investigation.',
  XC: 'FCRA direct dispute investigation completed — consumer disagrees with the results of the data furnisher’s investigation.',
  XD: 'Account closed at consumer’s request; and account information disputed by the consumer directly to the data furnisher under the FCRA; the data furnisher is conducting its investigation.',
  XE: 'Account closed at consumer’s request; and data furnisher has completed its investigation; consumer disagrees with the results of the investigation. ',
  XF: 'Account in dispute under Fair Credit Billing Act (FCBA); the data furnisher is conducting its investigation.',
  XG: 'FCBA dispute investigation completed — consumer disagrees with the results of the data furnisher’s investigation.',
  XH: 'Account previously in dispute; the data furnisher has completed its investigation.',
  XJ: 'Account closed at consumer’s request; and account information disputed by the consumer under FCBA; the data furnisher is conducting its investigation.',
  XR: 'Removes the most recently reported Compliance Condition Code'
}

export const K2_PURCHASED_SOLD_INDICATOR_LOOKUP = {
  '1': 'Purchased From Name',
  '2': 'Sold To Name',
  '9': 'Remove Previously Reported K2 Segment Information'
}

export const PORTFOLIO_TYPE_LOOKUP = {
  C: 'Line of Credit',
  I: 'Installment',
  M: 'Mortgage',
  O: 'Open',
  R: 'Revolving'
}

export const ACCOUNT_TYPE_LOOKUP = {
  '00': 'Auto',
  '01': 'Unsecured',
  '02': 'Secured',
  '03': 'Partially Secured',
  '04': 'Home Improvement',
  '05': 'FHA Home Improvement',
  '06': 'Installment Sales Contract',
  '07': 'Charge Account',
  '08': 'Real estate, specific type unknown',
  '10': 'Business Loan',
  '11': 'Recreational Merchandise',
  '12': 'Education',
  '13': 'Lease',
  '15': 'Line of Credit',
  '17': 'Manufactured Housing',
  '18': 'Credit Card',
  '19': 'FHA Real Estate Mortgage',
  '20': 'Note Loan',
  '25': 'VA Real Estate Mortgage',
  '26': 'Conventional Real Estate Mortgage',
  '29': 'Rental Agreement',
  '37': 'Combined Credit Plan',
  '43': 'Debit Card',
  '47': 'Credit Line Secured',
  '48': 'Collection Agency/Attorney',
  '50': 'Family Support',
  '65': 'Government Unsecured Guaranteed Loan',
  '66': 'Government Secured Guaranteed Loan',
  '67': 'Government Unsecured Direct Loan',
  '68': 'Government Secured Direct Loan',
  '69': 'Government Grant',
  '70': 'Government Overpayment',
  '71': 'Government Fine',
  '72': 'Government Fee for Services',
  '73': 'Government Employee Advance',
  '74': 'Government Misc. Debt',
  '75': 'Government Benefit',
  '77': 'Returned Check',
  '89': 'Home Equity Line of Credit',
  '90': 'Medical Debt',
  '91': 'Debt Consolidation',
  '92': 'Utility Company',
  '93': 'Child Support',
  '95': 'Attorney Fees',
  '0A': 'Time Share Loan',
  '2A': 'Secured Credit Card',
  '3A': 'Auto Lease',
  '5A': 'Real Estate — Junior Liens and Non-Purchase Money First',
  '6A': 'Commercial Installment Loan',
  '7A': 'Commercial Line of Credit',
  '8A': 'Business Credit Card',
  '9A': 'Secured Home Improvement',
  '5B': 'Second Mortgage',
  '6B': 'Commercial Mortgage Loan',
  '7B': 'Agricultural',
  '8B': 'Deposit Account with Overdraft Protection',
  '9B': 'Business Line Personally Guaranteed',
  '0C': 'Debt Buyer',
  '2C': 'U.S. Department of Agriculture (USDA) Real Estate Mortgage Loan',
  '4D': 'Telecommunications/Cellular',
  '6D': 'Home Equity',
  '0F': 'Export construction Loan',
  '0G': 'Flexible Spending Credit Card'
}

export const TERMS_FREQUENCY_LOOKUP = {
  D: 'Deferred (Refer to Note)',
  P: 'Single Payment Loan',
  W: 'Weekly',
  B: 'Biweekly',
  E: 'Semimonthly',
  M: 'Monthly',
  L: 'Bimonthly',
  Q: 'Quarterly',
  T: 'Triannually',
  S: 'Semiannually',
  Y: 'Annually'
}

export const CONSUMER_INFORMATION_INDICATOR_LOOKUP = {
  A: 'Petition for Chapter 7 Bankruptcy',
  B: 'Petition for Chapter 11 Bankruptcy',
  C: 'Petition for Chapter 12 Bankruptcy',
  D: 'Petition for Chapter 13 Bankruptcy',
  E: 'Discharged through Bankruptcy Chapter 7',
  F: 'Discharged through Bankruptcy Chapter 11',
  G: 'Discharged through Bankruptcy Chapter 12',
  H: 'Discharged/Completed through Bankruptcy Chapter 13',
  '1A': 'Personal Receivership',
  Q: 'Removes previously reported Bankruptcy Indicator or reports bankruptcy has been closed, terminated, dismissed or withdrawn, without being discharged.'
}

// Enables accessing a field's lookup by the field's id.
export const M2_FIELD_LOOKUPS = {
  acct_stat: ACCOUNT_STATUS_LOOKUP,
  acct_type: ACCOUNT_TYPE_LOOKUP,
  compl_cond_cd: COMPLIANCE_CONDTION_CODE_LOOKUP,
  k2_purch_sold_ind: K2_PURCHASED_SOLD_INDICATOR_LOOKUP,
  php: PAYMENT_HISTORY_PROFILE_LOOKUP,
  php1: PAYMENT_HISTORY_PROFILE_LOOKUP,
  pmt_rating: PAYMENT_RATING_LOOKUP,
  spc_com_cd: SPECIAL_COMMENT_CODE_LOOKUP,
  port_type: PORTFOLIO_TYPE_LOOKUP,
  terms_freq: TERMS_FREQUENCY_LOOKUP,
  j1__cons_info_ind: CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  j2__cons_info_ind: CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  account_holder__cons_info_ind: CONSUMER_INFORMATION_INDICATOR_LOOKUP
}
