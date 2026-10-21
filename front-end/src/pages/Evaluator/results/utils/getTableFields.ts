import M2_FIELD_NAMES from '@src/constants/m2FieldNames'

/**
getTableFields()
Generate list of fields that will appear as columns in the table for this evaluator's
results.

The fields are displayed in this order:
  - consumer account number, in a left-pinned column
  - activity date
  - all the fields that were used in the evaluator
  - filterable fields, prioritized by frequency of use
  - the rest of the fields from M2_FIELD_NAMES (which contains all the
    account record fields we use in the tool in the order they occur in the CRRG)

@param {array} fieldsUsed - list of fields used by this eval
@returns {array} Returns a list of fields that will be columns in the results table
*/

/**
Fields that identify a record and always come first in the table.
*/
export const identifierFields = ['cons_acct_num', 'activity_date']

/**
A list of the fields that are filterable on the evaluator page.
The first four fields are stakeholder-prioritized.
*/
export const filterableFields = [
  'acct_stat',
  'current_bal',
  'amt_past_due',
  'dofd',
  'compl_cond_cd',
  'php1',
  'php',
  'pmt_rating',
  'spc_com_cd',
  'terms_freq',
  'cons_info_ind',
  'cons_info_ind_assoc',
  'l1__change_ind',
  'date_closed'
]

export const getTableFields = (fieldsUsed: string[]): string[] => [
  ...new Set([
    ...identifierFields,
    // TODO: consider if we should filter out anything in fields_used
    // that isn't present in M2_FIELD_NAMES
    ...fieldsUsed,
    ...filterableFields,
    ...M2_FIELD_NAMES.keys()
  ])
]
