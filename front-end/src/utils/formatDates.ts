export const dateFormat = {
  default: {
    month: '2-digit',
    day: '2-digit',
    year: '2-digit',
    timeZone: 'UTC'
  },
  text: {
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC'
  }
}

/**
 * isDateString()
 *
 * Checks if a string is a valid date
 *
 * @param {number | string | null | undefined} val - a value
 * @returns {boolean} True if value is a valid date string; False otherwise
 * @examples
 *    - isDateString('1992-01-01')
 *      // True
 *    - isDateString('January 20, 1999')
 *      // True
 *    - isDateString(null)
 *      // False
 */
export const isDateString = (val: number | string | null | undefined): boolean =>
  !!val && !Number.isNaN(new Date(val).valueOf())

/**
 * formatDate()
 *
 * Given a valid date string, returns a string with specified date format.
 * Otherwise, returns empty string.
 *
 * @param {number | string | null | undefined} val - a value
 * @param {string} format - the format for the returned string
 * @returns {string} - Formatted date string if val is a valid date string
 *                   - Empty string for any other input
 * @examples
 *    - formatDate('2024-01-04')
 *      Returns: 01/04/24
 *
 *    - formatDate('2024-01-04', 'text')
 *      Returns: Jan 2024
 */
export const formatDate = (
  val: number | string | null | undefined,
  format: 'default' | 'text' = 'default'
): string => {
  if (!isDateString(val)) return ''
  return new Intl.DateTimeFormat(
    'en-US',
    dateFormat[format] as Intl.DateTimeFormatOptions
  ).format(new Date(String(val)))
}

/**
 * formatDateRange()
 *
 * Given two date strings, returns a data range string with provided format
 *
 * @param {number | string | null | undefined} start - start date for range
 * @param {number | string | null | undefined} end - end date for range
 * @param {string} format - the format for the returned string
 * @returns {string} - Formatted date range string if start and end are valid dates
 *                   - Empty string for any other input
 * @examples
 *  - formatDateRange('2024-01-01', '2024-02-01')
 *    Returns: 01/01/24 - 02/01/2024
 *
 *  - formatDateRange('2024-01-01', '2024-02-01', 'text')
 *    Returns: Jan 2024 - Feb 2024
 */
export const formatDateRange = (
  start: number | string | null | undefined,
  end: number | string | null | undefined,
  format: 'default' | 'text' = 'default'
): string =>
  isDateString(start) && isDateString(end)
    ? `${formatDate(start, format)} - ${formatDate(end, format)}`
    : ''
