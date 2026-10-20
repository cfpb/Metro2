/* eslint-disable unicorn/prefer-set-has */
import { M2_FIELD_LOOKUPS } from '@src/constants/annotationLookups'
import COL_DEF_CONSTANTS from '@src/constants/colDefConstants'
import { annotateM2FieldValue } from '@src/utils/annotations'
import { formatDate } from '@src/utils/formatDates'
import { formatNumber, formatUSD } from '@src/utils/formatNumbers'

// TODO: maybe generate the col definitions from a list of date and currency fields
// Derive a list of date fields from the account record column definitions
const dateFields = Object.keys(COL_DEF_CONSTANTS).filter(field => {
  const coldef = COL_DEF_CONSTANTS[field as keyof typeof COL_DEF_CONSTANTS]
  return 'type' in coldef && coldef.type === 'formattedDate'
})

// Derive a list of currency fields from the account record column definitions
const currencyFields = Object.keys(COL_DEF_CONSTANTS).filter(field => {
  const coldef = COL_DEF_CONSTANTS[field as keyof typeof COL_DEF_CONSTANTS]
  return 'type' in coldef && coldef.type === 'currency'
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
  if (value === null || value === undefined) return ''
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

// Generate the value that should be displayed in the CSV download
// for a specific field:
//    an annotated string for a value with an annotation lookup
//    a comma-joined string for an array
//    a string for a numerical value
//    and the raw value for anything else
export const getDownloadValue = (field: string, value: unknown): unknown => {
  // Numbers and strings can be formatted if of an appropriate field type
  if (value === null || value === undefined) return ''
  if (typeof value === 'string' || Number.isFinite(value)) {
    const val = value as string | number
    return annotatedFields.includes(field)
      ? annotateM2FieldValue(field, val)
      : String(val)
  }
  // Arrays should be converted to strings
  if (Array.isArray(value)) return value.join('')
  // Any other value should be returned as is
  return value
}

// const dateFields = ['activity_date', 'date_open', 'date_closed', 'doai', 'dofd', 'dolp', 'k4__deferred_pmt_st_dt', 'k4__balloon_pmt_due_dt', 'previous_values__activity_date', 'previous_values__date_open', 'previous_values__dofd', '']
// const COL_DEF_CONSTANTS = {
//   actual_pmt_amt: { type: 'currency' },
//   amt_past_due: { type: 'currency' },
//   credit_limit: { type: 'currency' },
//   current_bal: { type: 'currency' },
//   hcola: { type: 'currency' },

//   orig_chg_off_amt: { type: 'currency' },
//   smpa: { type: 'currency', minWidth: 140 },
//   k4__balloon_pmt_amt: { type: 'currency' },

//   previous_values__activity_date: { type: 'formattedDate', minWidth: 160 },
//   previous_values__date_open: { type: 'formattedDate', minWidth: 100 },
//   previous_values__dofd: { type: 'formattedDate', minWidth: 100 },
//   previous_values__date_closed: { type: 'formattedDate', minWidth: 110 },
//   previous_values__current_bal: { type: 'currency' },
//   previous_values__orig_chg_off_amt: { type: 'currency' }
// }
