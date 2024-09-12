/* eslint-disable unicorn/prefer-set-has */
import { M2_FIELD_LOOKUPS } from 'utils/annotationLookups'
import { COL_DEF_CONSTANTS } from 'utils/constants'
import { annotateValue, formatDate, formatUSD } from '../../src/utils/formatters'

// TODO: maybe generate the col definitions from a list of date and currency fields
// Derive a list of date fields from the account record column definitions
const dateFields = Object.keys(COL_DEF_CONSTANTS).filter(field => {
  const coldef = COL_DEF_CONSTANTS[field as keyof typeof COL_DEF_CONSTANTS]
  return 'type' in coldef ? coldef.type === 'formattedDate' : false
})

// Derive a list of currency fields from the account record column definitions
const currencyFields = Object.keys(COL_DEF_CONSTANTS).filter(field => {
  const coldef = COL_DEF_CONSTANTS[field as keyof typeof COL_DEF_CONSTANTS]
  return 'type' in coldef ? coldef.type === 'currency' : false
})

// Derive a list of annotated fields from the annotation lookup map
const annotatedFields = Object.keys(M2_FIELD_LOOKUPS)

// Generate the value that should be displayed in the account record table cell
// for a specific field:
//    a formatted date for a date field
//    a USD-formatted number for a currency field
//    an annotated string for a value with an annotation lookup
//    and the raw value for any other field
export const getDisplayValue = (
  field: string,
  value: number | string | null | undefined
): number | string | null | undefined => {
  if (currencyFields.includes(field)) return formatUSD(value)
  if (dateFields.includes(field)) return formatDate(value)
  if (annotatedFields.includes(field)) return annotateValue(field, value)
  return value
}
