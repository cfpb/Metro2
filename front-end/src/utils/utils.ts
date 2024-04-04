import { notFound } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type { M2_FIELDS } from './constants'
import {
  FIELD_NAMES_LOOKUP,
  FIELD_TYPES_LOOKUP,
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
  pinnedLeft: (typeof M2_FIELDS)[number][]
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
): Promise<TData> => {
  try {
    // Fetch data from URL.
    // If response is successful, return JSON.
    // If unsuccessful, throw an error with the response
    // status (404, 500, etc) as its message.
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

// TODO: formatters should only be called on numbers / null,
// but consider how / if to handle non-numeric values

// Given a number, returns a formatted numeric string
// Returns the raw value if any other data type is passed in
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function formatNumber(val: any): any {
  return typeof val === 'number' ? numberFormatter.format(val) : val
}

// Given a number, returns a USD-formatted string
// Returns the raw value if any other data type is passed in
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function formatUSD(val: any): any {
  return typeof val === 'number' ? currencyFormatter.format(val) : val
}
