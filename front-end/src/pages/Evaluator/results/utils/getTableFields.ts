import M2_FIELD_NAMES from '@src/constants/m2FieldNames'

/**
 * getTableFields()
 *
 * Generate list of fields that will appear as columns in the table for this evaluator's
 * results.
 *
 * The fields are displayed in this order:
 *   - consumer account number, in a left-pinned column
 *   - activity date
 *   - all the fields that were used in the evaluator
 *   - the rest of the fields from M2_FIELD_NAMES (which contains all the
 *     account record fields we use in the tool in the order they occur in the CRRG)
 *
 * @param {array} fields_used - list of fields used by this eval
 * @returns {array} Returns a list of fields that will be columns in the results table
 */

const getTableFields = (fields_used: string[]): string[] => [
  ...new Set([
    'cons_acct_num',
    'activity_date',
    ...fields_used,
    ...M2_FIELD_NAMES.keys()
  ])
]

export default getTableFields
