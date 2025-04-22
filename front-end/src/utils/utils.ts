import { notFound } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type Event from 'pages/Event/Event'
import type EvaluatorMetadata from 'types/Evaluator'
import type { AccountRecord } from './constants'
import { M2_FIELD_NAMES, PII_COOKIE_NAME } from './constants'

import { annotateValue, capitalized } from './formatters'

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
        : annotateValue(field, val ?? '')
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

// Given a string and a lookup map, returns either the string's value in the lookup
// or, if the string is not found in the lookup, a capitalized version of the string
export const getHeaderName = (
  field: string,
  lookup: Map<string, string> = M2_FIELD_NAMES
): string => lookup.get(field) ?? capitalized(field)

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
    headerName: getHeaderName(field),
    ...colDefProps[field]
  }))

/**
 * Fetches data from the API using provided URL.
 * Returns JSON from successful requests and throws
 * appropriate errors for unsuccessful ones.
 */
export const fetchData = async <TData>(
  url: string,
  dataType: string,
  delay?: number
): Promise<TData> => {
  try {
    // Fetch data from URL.
    // If response is successful, return JSON.
    // If unsuccessful, throw an error with the response
    // status (404, 500, etc) as its message.

    const response = await fetch(url)
    if (delay) {
      // Temporary hack to show loading view
      // eslint-disable-next-line no-promise-executor-return
      await new Promise(r => setTimeout(r, delay))
    }
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

/**
 * Stringifies values without quotation marks or encoding
 * @param {number | object | string} value - A value to stringify
 * @returns {string} A string
 */
export function customStringify(value: number | object | string): string {
  if (typeof value === 'string') return value
  if (typeof value === 'number') return String(value)
  if (Array.isArray(value)) return value.sort((a, b) => a - b).join(',')
  if (typeof value === 'object') return JSON.stringify(value).replaceAll('"', '')
  return ''
}

/**
 * Generates a human-readable query string from a search object
 * without encoding
 * @param {object} search - Search object
 * @returns {string} A query string or empty string
 */

export function stringifySearchParams(search: object | null | undefined): string {
  if (typeof search !== 'object' || search === null) return ''
  // Sort the items so they'll be in consistent order for react query
  const searchItems = Object.keys(search).sort()
  const searchParams = []
  for (const key of searchItems) {
    const value = search[key as keyof typeof search]
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    if (value !== null && value !== '') {
      searchParams.push(`${key}=${customStringify(value)}`)
    }
  }
  return searchParams.length > 0 ? `?${searchParams.join('&')}` : ''
}

/**
 *  Implements a custom parser to be used by tanstack router
 *  for parsing query strings instead of its default, JSON.parse().
 *
 *  Custom handling added in this parser:
 *    - Comma-separated lists of values are split into arrays.
 *      This allows us to serialize arrays with comma separation when
 *      generating query strings (eg, "acct_stat=11,13,61") and then
 *      turn them back into arrays when the query string is parsed.
 *
 * @param {string} search - The value of a query string key / value pair.
 *                          Only values that are strings are passed to this parser.
 *                          eg: Where query string = acct_stat=1,2,3&page=1,
 *                              '1,2,3' would be passed to this parser but 1 would not.
 * @returns {unknown} Returns an array if the search string contains a comma.
 *                    Otherwise, the output of JSON.parse()
 * @example
 * // Example input: '1,2,3'
 * // Expected output: ['1', '2', '3']
 */
export const customParser = (search: string): unknown => {
  if (search.includes(',')) return search.split(',')
  return JSON.parse(search)
}
