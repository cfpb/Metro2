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
