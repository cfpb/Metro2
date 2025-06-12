import type AccountRecord from 'types/AccountRecord'
import { M2_FIELD_LOOKUPS } from '../constants/annotationLookups'

/**
 * getM2Definition()
 *
 * Given a field name and value for a Metro2 field,
 * checks if there is a lookup for the field's codes.
 * If so, and the field's value is found in the lookup,
 * returns the definition corresponding with that value.
 * Otherwise, returns undefined.
 *
 * @param {string} field - the name of a Metro 2 field
 * @param {number | string | null | undefined} value - the field's value
 * @returns {string | undefined} definition for the value or undefined
 *
 */
export const getM2Definition = (
  field: string,
  value?: number | string | null
): string | undefined => {
  if (field in M2_FIELD_LOOKUPS && value != null) {
    const lookup = M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
    return lookup[value as keyof typeof lookup]
  }
  return undefined
}

/**
 * annotateM2FieldValue()
 *
 * Given a Metro2 field and value, calls getM2Definition to
 * check if there is a human-readable definition for the value.
 * If there is a definition, returns `value (definition)`
 * If no definition is available, returns the original value.
 *
 * @param {string} field - the name of a Metro 2 field
 * @param {number | string} val - the field's value
 * @returns {number | string} a string with format `value (annotation)`,
 *                            or the original value
 *
 */
export const annotateM2FieldValue = (
  field: string,
  val: number | string
): number | string => {
  const annotation = getM2Definition(field, val)
  return annotation ? `${val} (${annotation})` : val
}

/**
 * annotateAccountRecords()
 *
 * Takes an array of Metro 2 account records and adds annotations --
 * descriptions of coded values -- for fields that have pre-determined
 * lists of values.
 *
 * @param {array} records - array of account records
 * @returns {array} Array of account records with annotations added
 * @example input: [{acct_stat: '11'}, {acct_stat: '13}]
 *          output: [{acct_stat: '11 (0-29 days past the due date (current account))'},
 *                   {acct_stat: '13 (Paid or closed account/zero balance)'}]
 *
 */
export const annotateAccountRecords = (records: AccountRecord[]): AccountRecord[] =>
  records.map((record: AccountRecord): AccountRecord => {
    // Create new object to hold the annotated values
    const obj: Record<string, unknown[] | number | string | null | undefined> = {}

    // Add a value for each field to the new object, with annotation if available.
    // If the original value is an array, annotate each item in the new array.
    for (const field of Object.keys(record)) {
      const val = record[field as keyof AccountRecord]
      obj[field] = Array.isArray(val)
        ? val.map((item: number | string): number | string | null | undefined =>
            annotateM2FieldValue(field, item)
          )
        : annotateM2FieldValue(field, val ?? '')
    }

    // Return annotated copy of record
    return obj
  })
