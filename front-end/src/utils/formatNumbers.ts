export function isNumeric(value: unknown) {
  return value !== '' && value !== null && Number.isFinite(Number(value))
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

/**
formatNumber()

Formats a number as a string

@param {string | number | null | undefined} val - a value
@returns {string | number | null | undefined} - Formatted numeric string if given a numeric value
                                                Original value for any other type
@examples
   Input: 1234567
   Output: 1,234,567
   Input: 'anything else'
   Output: ''
*/
export function formatNumber(val: string | number | null | undefined): string | number | null | undefined {
  return isNumeric(val) ? numberFormatter.format(Number(val)) : val
}

/**
formatUSD()

Applies US currency formatting to a number

@param {string | number | null | undefined} val - a value
@returns {string | number | null | undefined} - USD-formatted numeric string if given a numeric value
                                                Original value for any other type
@examples
   Input: '1234567'
   Output: $1,234,567
   Input: 1234567.4567
   Output: $1,234,567.46
   Input: anything else
   Output: original value
*/
export function formatUSD(val: string | number | null | undefined): string | number | null | undefined {
  return isNumeric(val) ? currencyFormatter.format(Number(val)) : val
}
