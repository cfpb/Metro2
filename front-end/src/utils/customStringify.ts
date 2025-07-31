/**
 * customStringify()
 *
 * Stringifies values without quotation marks or encoding
 *
 * Input     Output
 * string    trimmed string
 * number    number as string
 * array     comma-separated string of values, sorted alphabetically
 * object    result of JSON.stringify(object)
 *
 * @param {number | object | string} value - A value to stringify
 * @returns {string} A string
 */
export function customStringify(
  value: number | object | string | null | undefined
): string {
  if (typeof value === 'string') return value.trim()
  if (typeof value === 'number') return String(value)
  if (Array.isArray(value)) return value.sort().join(',')
  if (value && typeof value === 'object') return JSON.stringify(value)
  return ''
}

/**
 * stringifySearchParams()
 *
 * Generates a human-readable query string from a search object
 * without encoding
 *
 * @param {object} search - Search object
 * @returns {string} A query string or empty string
 */

export function stringifySearchParams(search: object | null | undefined): string {
  if (typeof search !== 'object' || search === null) return ''

  // Sort the items so they'll be in consistent order for react query
  const searchItems = Object.keys(search).sort()

  // For items with a non-null value, add a `key=stringified value` segment to a new array.
  const searchParams = []
  for (const key of searchItems) {
    const value = search[key as keyof typeof search]
    if (![null, '', undefined].includes(value))
      searchParams.push(`${key}=${customStringify(value)}`)
  }

  // If there are any segments in array, join & return. Otherwise, return empty string.
  return searchParams.length > 0 ? `?${searchParams.join('&')}` : ''
}
