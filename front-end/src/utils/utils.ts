import { notFound } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type { AccountRecord } from './constants'
import {
  FIELD_NAMES_LOOKUP,
  FIELD_TYPES_LOOKUP,
  M2_FIELDS,
  M2_FIELD_LOOKUPS
} from './constants'

/**
 * Takes an id and value for a Metro2 field,
 * accesses the lookup for the field's code definitions,
 * and returns either the definition corresponding with
 * the value provided for the field or undefined.
 */
export const getM2Definition = (
  fieldId: string,
  fieldValue?: number | string | null
): string | undefined => {
  if (fieldValue != null && fieldId in M2_FIELD_LOOKUPS) {
    const lookup = M2_FIELD_LOOKUPS[fieldId as keyof typeof M2_FIELD_LOOKUPS]
    return lookup[fieldValue as keyof typeof lookup]
  }
  return undefined
}

// Iterates through array of account records and adds parenthetical
// annotations to record's values where they exist
export const annotateData = (records: AccountRecord[]): AccountRecord[] =>
  records.map(record => {
    const obj: Record<string, number | string | null | undefined> = {}
    for (const field of Object.keys(record)) {
      const val = record[field as keyof AccountRecord]
      const annotation = getM2Definition(field, val)
      obj[field] = annotation ? `${val} (${annotation})` : val
    }
    return obj
  })

// Checks whether a string is in the list of Metro 2 fields
export const isM2Field = (str: string): boolean => !!M2_FIELDS.includes(str)

// Annotate and add php1 to account record data
export const prepareAccountRecordData = (
  records: AccountRecord[]
): AccountRecord[] => {
  if ('php' in records[0]) {
    for (const record of records) record.php1 = record.php?.charAt(0)
  }
  return annotateData(records)
}

// Given a list of M2 fields and a list of M2 fields to pin,
// generate an array of AgGrid column definition objects
// with the following format:
// {
//    field: field,
//    headerName: field's name from FIELD_NAMES_LOOKUP,
//    type: field's type from FIELD_TYPES_LOOKUP,
//    pinned: 'left' if field is in pinnedLeft array
// }
export const generateColumnDefinitions = (
  // all the values in these arrays should appear in the M2_FIELDS list
  fields: (typeof M2_FIELDS)[number][],
  pinnedLeft: (typeof M2_FIELDS)[number][] = []
): ColDef[] =>
  fields.map(field => ({
    field,
    headerName: FIELD_NAMES_LOOKUP[field as keyof typeof FIELD_NAMES_LOOKUP],
    type: FIELD_TYPES_LOOKUP[field as keyof typeof FIELD_TYPES_LOOKUP],
    pinned: pinnedLeft.includes(field) ? 'left' : undefined
  }))

/**
 * Fetches data from the API using provided URL.
 * Returns JSON from successful requests and throws
 * appropriate errors for unsuccessful ones.
 */
export const fetchData = async <TData>(
  url: string,
  dataType: string
  // delay?: number
): Promise<TData> => {
  try {
    // Fetch data from URL.
    // If response is successful, return JSON.
    // If unsuccessful, throw an error with the response
    // status (404, 500, etc) as its message.

    // if (delay) {
    //   // Temporary hack to show loading view
    //   // eslint-disable-next-line no-promise-executor-return
    //   await new Promise(r => setTimeout(r, delay))
    // }

    const response = await fetch(url)
    if (response.ok) return (await response.json()) as TData
    throw new Error(String(response.status))
  } catch (error) {
    // Throw NotFound error to handle 404s in NotFound component
    // All other errors will be caught by ErrorComponent
    const message = error instanceof Error ? error.message : ''
    if (message === '404') notFound({ throw: true, data: dataType })
    throw new Error(message)
  }
}

export const numberFormatter = new Intl.NumberFormat('en-US', {
  notation: 'standard'
})

export const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
})

// Given a number, returns a formatted numeric string
// Returns empty string if any other data type is passed in
export function formatNumber(val: number | null | undefined): string {
  return typeof val === 'number' ? numberFormatter.format(val) : ''
}

// Given a number, returns a USD-formatted string
// Returns empty string if any other data type is passed in
export function formatUSD(val: number | null | undefined): string {
  return typeof val === 'number' ? currencyFormatter.format(val) : ''
}

// Given a date string in format yyyy-mm-dd, returns a mm/dd/yyyy formatted string
// Returns empty string if any other data type is passed in
export const formatDate = (val: string | null | undefined): string =>
  typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)
    ? new Date(`${val}T00:00:00`).toLocaleDateString('en-us')
    : ''

// Takes an ordered list of fields, a header lookup, and an array of records
// Generates header by getting values for each field from the header lookup
// (doing the lookup here seems safer: both header and body rows get their order
// from the list of fields)
// Outputs a CSV containing header and each record's data for the provided fields
export const generateDownloadData = <T>(
  fields: string[],
  records: T[],
  headerLookup: Record<string, string>
): string => {
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
  const csvHeader = fields.map(field => headerLookup[field] ?? field).join(',')
  const csvBody = records
    .map(record =>
      fields
        .map(field => {
          const val = record[field as keyof T]
          return Array.isArray(val) ? val.join('; ') : val
        })
        .join(',')
    )
    .join('\n')
  return [csvHeader, csvBody].join('\n')
}

// Takes a comma-formatted CSV string and a suggested file name,
// opens a file picker prompting the user to download the
// CSV to the documents directory with the suggested name,
// and writes the file to the user's system if they select save
export const downloadData = async (
  csvString: string,
  fileName: string
): Promise<void> => {
  const handle = await showSaveFilePicker({
    suggestedName: fileName,
    // @ts-expect-error Typescript doesn't handle File System API well
    startIn: 'documents',
    types: [
      {
        description: 'CSVs',
        accept: {
          'text/csv': ['.csv']
        }
      }
    ]
  })
  const writable = await handle.createWritable()
  await writable.write(csvString)
  return writable.close()
}

// Generates html for an evaluator long description that is only formatted with line breaks.
// Splits string into segments at double line breaks. Breaks segments into lines.
// If the first line of a segment is explanatory rather than pseudo-code
// -- determined by checking for absence of symbols used in pseudo code lines --
// it's formatted as an H4. All other lines are formatted as paragraphs.
export const formatLongDescription = (longDescription: string): string => {
  let html = ''
  for (const segment of longDescription.split('\n\n')) {
    for (const [lineIndex, line] of segment.split('\n').entries()) {
      const isHeader =
        lineIndex === 0 &&
        ![':', '<', '>', '=', '≠'].some(char => line.includes(char))
      html += `<${isHeader ? 'h4' : 'p'}>${line}</${isHeader ? 'h4' : 'p'}>`
    }
  }
  return html
}
