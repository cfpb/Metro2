import { currencyFormatter } from './formatNumbers'

// Given a number, returns a USD-formatted string
// Returns empty string if any other data type is passed in
export function formatUSD(val: number | string | null | undefined): string {
  return typeof val === 'number' ? currencyFormatter.format(val) : ''
}

const isDateString = (val: number | string | null | undefined): boolean =>
  typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)

// Given a date string in format yyyy-mm-dd, returns a date string
// formatted according to 'format' param
// text: January 2024
// abbreviatedText: Jan 2024
// default: 01/04/24
// Returns empty string if any other data type is passed in
export const formatDate = (
  val: number | string | null | undefined,
  format?: string | null | undefined
): string => {
  if (!isDateString(val)) return ''
  if (format === 'text') {
    return new Date(`${val}T00:00:00`).toLocaleDateString('en-us', {
      month: 'long',
      year: 'numeric'
    })
  }
  if (format === 'abbreviatedText') {
    return new Date(`${val}T00:00:00`).toLocaleDateString('en-us', {
      month: 'short',
      year: 'numeric'
    })
  }
  return new Date(`${val}T00:00:00`).toLocaleDateString('en-us', {
    month: '2-digit',
    day: '2-digit',
    year: '2-digit'
  })
}

export const formatDateRange = (
  start: string | null,
  end: string | null,
  format?: 'abbreviatedText' | 'text'
): string =>
  start && end ? `${formatDate(start, format)} - ${formatDate(end, format)}` : ''
