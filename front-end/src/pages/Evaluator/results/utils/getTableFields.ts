import M2_FIELD_NAMES from '@src/constants/m2FieldNames'

const defaultFields = [
  // 'id',
  'doai',
  'acct_stat',
  'compl_cond_cd',
  'php',
  'php1',
  'pmt_rating',
  'spc_com_cd',
  'terms_freq',
  'dofd',
  'date_closed',
  'amt_past_due',
  'current_bal',
  'account_holder__cons_info_ind',
  'account_holder__cons_info_ind_assoc',
  'l1__change_ind'
]

const matchListOrder = (list: string[], order: string[]): string[] =>
  list.sort((a, b) => (order.indexOf(a) > order.indexOf(b) ? 1 : -1))

/**
 * getTableFields()
 *
 * Generate list of fields that will appear as columns in the table for this evaluator's
 * results.
 *
 * The results table for each evaluator shows a custom subset of M2 fields that are useful
 * for understanding the scenario the specific evaluator is targeting.
 *
 * The list of fields displayed in the table is created by combining two lists from the evaluator's metadata
 * (fields_used--fields that are actually checked by the evaluator, & fields_display--other helpful fields)
 * with some default fields that are shown for each evaluator.
 *
 * Then we sort the list of fields by the order of the keys in M2_FIELD_NAMES to match
 * the order of the fields in the M2 data, and add a field for the first character of PHP
 * (one of the default fields) directly after the index of PHP.
 * (We use the first character of the 24 character payment history profile field in evaluators,
 * but php1 values are separated out on the front end and not returned from the API.)
 *
 * @param {array} fields_used - list of fields used by this eval
 * @param {array} fields_display - list of fields that are also relevant to this eval
 * @returns {array} Returns a list of fields that will be columns in the results table
 */

const getTableFields = (
  fields_used: string[],
  fields_display: string[]
): string[] => {
  const order = [...M2_FIELD_NAMES.keys()]
  const fieldsUsed = matchListOrder(fields_used, order)
  const additionalFields = matchListOrder(
    [...fields_display, ...defaultFields],
    order
  )
  const tableFields = [
    ...new Set([
      'cons_acct_num',
      'activity_date',
      ...fieldsUsed,
      ...additionalFields
    ])
  ]
  return tableFields
}

export default getTableFields
