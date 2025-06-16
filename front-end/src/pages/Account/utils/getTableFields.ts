import M2_FIELD_NAMES from '../../../constants/m2FieldNames'

// Get fields from M2_FIELD_NAMES
// remove cons_acct_num since we're not currently getting it on each record
// from the account API endpoint
// remove account holder name values
// remove all the prior value fields since they'll be displayed in the adjacent row
// and add 'inconsistencies' at position 2
const getTableFields = (): string[] => {
  const fields = [...M2_FIELD_NAMES.keys()].filter(
    field =>
      ![
        'cons_acct_num',
        'account_holder__first_name',
        'account_holder__surname'
      ].includes(field) && !field.startsWith('previous_values')
  )
  fields.splice(1, 0, 'inconsistencies')
  return fields
}

export default getTableFields
