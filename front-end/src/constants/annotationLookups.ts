/**
 * Many Metro2 fields contain coded values that need to be translated
 * into a more human-readable format for display in the Metro2 tool.
 *
 * The following lookups map a field's possible coded values to their
 * definitions.
 *
 */

export const ACCOUNT_STATUS_LOOKUP = {
  '05': 'Transferred',
  '11': '0-29 days past the due date (current account)',
  '13': 'Paid or closed account/zero balance',
  '61': 'Paid in full, was a voluntary surrender',
  '62': 'Paid in full, was a collection account',
  '63': 'Paid in full, was a repossession',
  '64': 'Paid in full, was a charge-off',
  '65': 'Paid in full. A foreclosure was started.',
  '71': '30-59 days past the due date',
  '78': '60-89 days past the due date',
  '80': '90-119 days past the due date',
  '82': '120-149 days past the due date',
  '83': '150-179 days past the due date',
  '84': '180 days or more past the due date',
  '88': 'Claim filed with government for insured portion of balance on a defaulted loan',
  '89': 'Deed received in lieu of foreclosure on a defaulted mortgage; there may be a balance due',
  '93': 'Assigned to internal or external collections',
  '94': 'Foreclosure completed; there may be a balance due',
  '95': 'Voluntary surrender; there may be a balance due',
  '96': 'Merchandise was repossessed; there may be a balance due',
  '97': 'Unpaid balance reported as a loss (charge-off)',
  DA: 'Delete entire account (for reasons other than fraud)',
  DF: 'Delete entire account due to confirmed fraud (fraud investigation completed)'
}

const L1_CHANGE_INDICATOR_LOOKUP = {
  '1': 'Consumer Account Number Change ONLY',
  '2': 'Identification Number Change ONLY',
  '3': 'Consumer Account Number AND Identification Number Change'
}

export const PAYMENT_RATING_LOOKUP = {
  '0': '0–29 days past the due date (current account)',
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
  XB: 'Data furnisher conducting investigation after consumer disputed account information under FCRA',
  XC: 'FCRA dispute investigation completed; consumer disagrees',
  XD: 'Account closed at consumer’s request; data furnisher conducting investigation after consumer disputed account information under FCRA',
  XE: 'Account closed at consumer’s request; data furnisher completed its investigation; consumer disagrees with results ',
  XF: 'Data furnisher conducting investigation after consumer disputed account information under FCBA',
  XG: 'FCBA dispute investigation completed; consumer disagrees',
  XH: 'Account previously in dispute; investigation completed',
  XJ: 'Account closed at consumer’s request; data furnisher conducting investigation after consumer disputed account information under FCBA',
  XR: 'Removes most recently reported code'
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

export const ECOA_CODE_LOOKUP = {
  '1': 'Individual',
  '2': 'Joint contractual liability',
  '3': 'Authorized user',
  '5': 'Co-maker or guarantor',
  '7': 'Maker',
  T: 'Terminated',
  X: 'Deceased',
  W: 'Business / Commercial',
  Z: 'Delete consumer'
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
  D: 'Deferred',
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
  Q: 'Removes previously reported Bankruptcy Indicator or reports bankruptcy has been closed, terminated, dismissed or withdrawn, without being discharged.',
  R: 'Chapter 7 Reaffirmation of Debt',
  S: 'Removes previously reported Reaffirmation of Debt, Reaffirmation of Debt Rescinded and Lease Assumption Indicators (R, V, 2A, and obsolete values W, X, Y)',
  T: 'Credit Grantor Cannot Locate Consumer',
  U: 'Consumer Now Located (Removes previously reported T Indicator)',
  V: 'Chapter 7 Reaffirmation of Debt Rescinded',
  '1A': 'Personal Receivership',
  '2A': 'Lease Assumption'
}

export const INTEREST_TYPE_INDICATOR_LOOKUP = {
  F: 'Fixed',
  V: 'Variable/Adjustable'
}

// Enables accessing a field's lookup by the field's id.
export const M2_FIELD_LOOKUPS = {
  acct_stat: ACCOUNT_STATUS_LOOKUP,
  acct_type: ACCOUNT_TYPE_LOOKUP,
  compl_cond_cd: COMPLIANCE_CONDTION_CODE_LOOKUP,
  int_type_ind: INTEREST_TYPE_INDICATOR_LOOKUP,
  php: PAYMENT_HISTORY_PROFILE_LOOKUP,
  php1: PAYMENT_HISTORY_PROFILE_LOOKUP,
  pmt_rating: PAYMENT_RATING_LOOKUP,
  port_type: PORTFOLIO_TYPE_LOOKUP,
  spc_com_cd: SPECIAL_COMMENT_CODE_LOOKUP,
  terms_freq: TERMS_FREQUENCY_LOOKUP,
  account_holder__cons_info_ind: CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  account_holder__cons_info_ind_assoc: CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  account_holder__ecoa: ECOA_CODE_LOOKUP,
  account_holder__ecoa_assoc: ECOA_CODE_LOOKUP,
  k2__purch_sold_ind: K2_PURCHASED_SOLD_INDICATOR_LOOKUP,
  l1__change_ind: L1_CHANGE_INDICATOR_LOOKUP,
  previous_values__account_holder__cons_info_ind:
    CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  previous_values__account_holder__cons_info_ind_assoc:
    CONSUMER_INFORMATION_INDICATOR_LOOKUP,
  previous_values__account_holder__ecoa: ECOA_CODE_LOOKUP,
  previous_values__l1__change_ind: L1_CHANGE_INDICATOR_LOOKUP,
  previous_values__port_type: PORTFOLIO_TYPE_LOOKUP,
  previous_values__acct_type: ACCOUNT_TYPE_LOOKUP,
  previous_values__acct_stat: ACCOUNT_STATUS_LOOKUP,
  previous_values__pmt_rating: PAYMENT_RATING_LOOKUP
}
