import { M2_FIELD_LOOKUPS } from './annotationLookups'

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

// Capitalizes first letter of a string
export const capitalized = (str: string): string =>
  `${str[0].toUpperCase()}${str.slice(1)}`

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
export function formatNumber(val: number | string | null | undefined): string {
  return typeof val === 'number' ? numberFormatter.format(val) : ''
}

// Given a number, returns a USD-formatted string
// Returns empty string if any other data type is passed in
export function formatUSD(val: number | string | null | undefined): string {
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
  val: number | string | null | undefined,
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
