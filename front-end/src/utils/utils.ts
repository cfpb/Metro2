import { notFound } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type EvaluatorMetadata from 'pages/Evaluator/Evaluator'
import type Event from 'pages/Event/Event'
import {
  AccountRecord,
  M2_FIELD_LOOKUPS,
  M2_FIELD_NAMES,
  PII_COOKIE_NAME
} from './constants'
/**
 * Takes an id and value for a Metro2 field,
 * accesses the lookup for the field's code definitions,
 * and returns either the definition corresponding with
 * the value provided for the field or undefined.
 */
export const getM2Definition = (
  field: string,
  value?: number | string | null
): string | undefined => {
  if (value != null && field in M2_FIELD_LOOKUPS) {
    const lookup = M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
    return lookup[value as keyof typeof lookup]
  }
  return undefined
}

// Given a Metro2 field and value, checks if there is a human-readable definition for the value.
// If there is a definition, returns a string with format 'value (definition)'
// If no definition is available, returns the original value
export const annotateValue = (
  field: string,
  val: number | string | null | undefined
): number | string | null | undefined => {
  const annotation = getM2Definition(field, val)
  return annotation ? `${val} (${annotation})` : val
}

// Iterates through array of account records and annotates values as needed
export const annotateAccountRecords = (records: AccountRecord[]): AccountRecord[] =>
  records.map((record: AccountRecord): AccountRecord => {
    // Create new object to hold the annotated values
    const obj: Record<string, unknown[] | number | string | null | undefined> = {}
    for (const field of Object.keys(record)) {
      // Add a value for each field to the new object, with annotation if available.
      // If the original value is an array, annotate each item in the new array.
      const val = record[field as keyof AccountRecord]
      obj[field] = Array.isArray(val)
        ? val.map((item: number | string): number | string | null | undefined =>
            annotateValue(field, item)
          )
        : annotateValue(field, val)
    }
    return obj
  })

// If the first record has a php value, add php1 to the records
export const addPHP1 = (records: AccountRecord[]): AccountRecord[] => {
  if (records.length <= 0 || !('php' in records[0])) return records
  return records.map(
    (record: AccountRecord): AccountRecord => ({
      ...record,
      php1: record.php?.charAt(0)
    })
  )
}

/**
 * Given an array of M2 account records, makes some updates for display in tables:
 *   1. if records include 'php' value, add 'php1' field containing first character of php
 *   2. add descriptive annotations to records for fields with coded values
 * Returns updated records
 */
export const prepareAccountRecordData = (
  records: AccountRecord[]
): AccountRecord[] => {
  // If the first record has a php value, add php1 to the records
  // if ('php' in records[0]) {
  //   for (const record of records) record.php1 = record.php?.charAt(0)
  // }
  const updatedRecords = addPHP1(records)
  // annotate coded record values
  return annotateAccountRecords(updatedRecords)
}

// Capitalizes first letter of a string
export const capitalized = (str: string): string =>
  `${str[0].toUpperCase()}${str.slice(1)}`

// Given a string and a lookup map, returns either the string's value in the lookup
// or, if the string is not found in the lookup, a capitalized version of the string
export const getHeaderName = (field: string, lookup: Map<string, string>): string =>
  lookup.get(field) ?? capitalized(field)

// Given a list of M2 fields and an object of field-specific col def props,
// generate an array of AgGrid column definition objects
// with the following format:
// {
//    field: field,
//    headerName: field's name from M2_FIELD_NAMES,
//    ...{field-specific col def props}
// }
export const generateColumnDefinitions = (
  fields: string[],
  colDefProps: Record<string, object>
): ColDef[] =>
  fields.map(field => ({
    field,
    headerName: getHeaderName(field, M2_FIELD_NAMES),
    ...colDefProps[field]
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

// // Given a date string in format yyyy-mm-dd, returns a mm/dd/yyyy formatted string
// // Returns empty string if any other data type is passed in
// export const formatDate = (val: string | null | undefined): string =>
//   typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)
//     ? new Date(`${val}T00:00:00`).toLocaleDateString('en-us')
//     : ''

// Given a date string in format yyyy-mm-dd, returns a mm/dd/yyyy formatted string
// Returns empty string if any other data type is passed in
export const formatDate = (
  val: string | null | undefined,
  shorthandDate = false
): string => {
  if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)) {
    return new Date(`${val}T00:00:00`).toLocaleDateString(
      'en-us',
      shorthandDate
        ? { month: 'short', year: 'numeric' }
        : { month: '2-digit', day: '2-digit', year: '2-digit' }
    )
  }
  return ''
}

// Takes an ordered list of fields, a header lookup, and an array of records
// Generates header by getting values for each field from the header lookup
// (doing the lookup here seems safer: both header and body rows get their order
// from the list of fields)
// Outputs a CSV containing header and each record's data for the provided fields
export const generateDownloadData = <T>(
  fields: string[],
  records: T[],
  headerMap: Map<string, string>
): string => {
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
  const csvHeader = fields.map(field => getHeaderName(field, headerMap)).join(',')
  const csvBody = records
    .map(record =>
      fields
        .map(field => {
          const val = record[field as keyof T]
          if (typeof val === 'string' && val.includes(',')) return `"${val}"`
          if (Array.isArray(val)) return `"${val.join(', ')}"`
          return val
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
    startIn: 'downloads',
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

export const downloadFileFromURL = (url: string): void => {
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.click()
}

// export const writeURLToFile = async (
//   fileName: string,
//   url: string
// ): Promise<void> => {
//   const handle = await showSaveFilePicker({
//     suggestedName: fileName,
//     // @ts-expect-error Typescript doesn't handle File System API well
//     startIn: 'documents',
//     types: [
//       {
//         description: 'CSVs',
//         accept: {
//           'text/csv': ['.csv']
//         }
//       }
//     ]
//   })
//   // Create a FileSystemWritableFileStream to write to.
//   const writable = await handle.createWritable()

//   try {
//     const response = await fetch(url)
//     // Stream the response into the file.
//     // pipeTo() closes the destination pipe by default, no need to close it.
//     if (response.ok) return await response.body?.pipeTo(writable)
//     throw new Error(String(response.status))
//   } catch (error) {
//     console.log(error)
//   }
// }
// Generates html for an evaluator long description that is only formatted with line breaks.
// Splits string into segments at double line breaks. Breaks segments into lines.
// If the first line of a segment is explanatory rather than pseudo-code
// -- determined by checking for absence of symbols used in pseudo code lines --
// it's formatted as an H4. All other lines are formatted as paragraphs.
export const formatLongDescription = (longDescription: string): string => {
  if (!longDescription) return ''
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

// Given a cookie name, value, and expire time (in days), sets a cookie.
// Expire time defaults to 1 day.
// TODO: consider whether to use cookieStore API (not supported in Safari)
export const setCookie = (
  cookieName: string,
  cookieValue: boolean | number | string,
  expires = 1
): void => {
  // eslint-disable-next-line unicorn/no-document-cookie
  document.cookie = `${cookieName}=${cookieValue}; max-age=${expires * 86_400}`
}

// Given a cookie name, retrieves cookie value
// TODO: consider whether to use cookieStore API (not supported in Safari)
export const getCookie = (cookieName: string): string | undefined =>
  // eslint-disable-next-line unicorn/no-document-cookie
  document.cookie
    .split('; ')
    .find(item => item.startsWith(`${cookieName}=`))
    ?.split('=')[1]

// Sets a cookie to reflect that the PII warning has been acknowledged
// Cookie expires in 1 day
export const acceptPIIWarning = (): void => {
  setCookie(PII_COOKIE_NAME, true)
}

// Checks for a cookie indicating PII warning has been acknowledged
export const hasAcceptedPIIWarning = (): boolean => !!getCookie(PII_COOKIE_NAME)

export const getEvaluatorDataFromEvent = (
  data: Event,
  evaluatorId: string
): EvaluatorMetadata | undefined =>
  data.evaluators.find((item: EvaluatorMetadata) => item.id === evaluatorId)
