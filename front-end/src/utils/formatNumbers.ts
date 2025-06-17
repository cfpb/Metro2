export const numberFormatter = new Intl.NumberFormat('en-US', {
  notation: 'standard'
})

export const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
})

/**
 * formatNumber()
 *
 * Formats a number as a string
 *
 * @param {number | string | null | undefined} val - a value
 * @returns {string} - Formatted numeric string if given a number
 *                     Empty string for any other data type
 * @examples
 *    Input: 1234567
 *    Output: 1,234,567
 *    Input: 'anything else'
 *    Output: ''
 */
export function formatNumber(val: number | string | null | undefined): string {
  return typeof val === 'number' ? numberFormatter.format(val) : ''
}

/**
 * formatUSD()
 *
 * Applies US currency formatting to a number
 *
 * @param {number | string | null | undefined} val - a value
 * @returns {string} - USD-formatted numeric string if given a number
 *                     Empty string for any other data type
 * @examples
 *    Input: 1234567
 *    Output: $1,234,567
 *    Input: 1234567.4567
 *    Output: $1,234,567.46
 *    Input: 'anything else'
 *    Output: ''
 */
export function formatUSD(val: number | string | null | undefined): string {
  return typeof val === 'number' ? currencyFormatter.format(val) : ''
}
