/* eslint-disable unicorn/prefer-set-has */
import { M2_FIELD_LOOKUPS } from 'constants/annotationLookups'
import COL_DEF_CONSTANTS from 'constants/colDefConstants'
import { annotateM2FieldValue } from 'utils/annotations'
import { formatDate } from 'utils/formatDates'
import { formatNumber, formatUSD } from 'utils/formatNumbers'

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
//    a comma-joined string for an array
//    and the raw value for anything else
export const getDisplayValue = (field: string, value: unknown): unknown => {
  // Numbers and strings can be formatted if of an appropriate field type
  if (typeof value === 'string' || Number.isFinite(value)) {
    const val = value as string | number
    if (currencyFields.includes(field)) return formatUSD(val)
    if (dateFields.includes(field)) return formatDate(val)
    if (annotatedFields.includes(field)) return annotateM2FieldValue(field, val)
    if (['hits', 'accounts_affected'].includes(field)) return formatNumber(val)
  }
  // Arrays should be converted to strings
  if (Array.isArray(value)) return value.join('')
  // Any other value should be returned as is
  return value
}
