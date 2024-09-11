import { annotateValue, formatDate, formatUSD } from '../../src/utils/formatters'
export const dateFields = [
  'activity_date',
  'date_open',
  'date_closed',
  'doai',
  'dofd',
  'dolp',
  'previous_values__activity_date',
  'previous_values__date_open',
  'previous_values__dofd',
  'previous_values__date_closed'
]

export const currencyFields = [
  'actual_pmt_amt',
  'amt_past_due',
  'credit_limit',
  'current_bal',
  'hcola',
  'orig_chg_off_amt',
  'smpa',
  'k4__balloon_pmt_amt',
  'previous_values__current_bal',
  'previous_values__orig_chg_off_amt'
]

export const annotatedFields = [
  'acct_stat',
  'acct_type',
  'compl_cond_cd',
  'php',
  'php1',
  'pmt_rating',
  'port_type',
  'spc_com_cd',
  'terms_freq',
  'account_holder__cons_info_ind',
  'account_holder__cons_info_ind_assoc',
  'account_holder__ecoa',
  'account_holder__ecoa_assoc',
  'k2__purch_sold_ind',
  'l1__change_ind',
  'previous_values__account_holder__cons_info_ind',
  'previous_values__account_holder__cons_info_ind_assoc',
  'previous_values__account_holder__ecoa',
  'previous_values__l1__change_ind',
  'previous_values__port_type',
  'previous_values__acct_type',
  'previous_values__acct_stat',
  'previous_values__pmt_rating'
]

export const getDisplayValue = (
  field: string,
  value: number | string | null | undefined
): number | string | null | undefined => {
  if (currencyFields.includes(field)) return formatUSD(value)
  if (dateFields.includes(field)) return formatDate(value)
  if (annotatedFields.includes(field)) return annotateValue(field, value)
  return value
}
