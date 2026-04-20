import M2_FIELD_NAMES from '@src/constants/m2FieldNames'

/**
 * Generate list of Metro 2 fields to be used as columns in the account table.
 *
 * - Get all fields from M2_FIELD_NAMES
 * - Remove cons_acct_num since it's not included on each record from the API
 * - Remve the account holder name values since we don't show them in the table
 * - Remove all the prior value fields since they'll be in adjacent rows
 * - Add 'Inconsistencies' as the second item in list
 *
 */

const accountTableFields = [...M2_FIELD_NAMES.keys()].filter(
  field =>
    !['cons_acct_num', 'first_name', 'surname'].includes(field) &&
    !field.startsWith('previous_values')
)
accountTableFields.splice(1, 0, 'inconsistencies')
export { accountTableFields }
