/**
 * customParser()
 *
 * Implements a custom parser to be used by tanstack router
 * for parsing query strings instead of its default JSON.parse.
 *
 * Custom handling added in this parser:
 *    - Comma-separated lists of values are split into arrays.
 *      This allows us to serialize arrays with comma separation when
 *      generating query strings (eg, "acct_stat=11,13,61") and then
 *      turn them back into arrays when the query string is parsed.
 *
 * @param {string} value - The value of a query string key / value pair.
 *                         Only values that are strings are passed to this parser.
 *                         eg: Where query string = acct_stat=1,2,3&page=1,
 *                             '1,2,3' would be passed to this parser but 1 would not.
 * @returns {unknown} Returns an array if the search string contains a comma.
 *                    Otherwise, the output of JSON.parse()
 * @example
 * // Example input: '1,2,3'
 * // Expected output: ['1', '2', '3']
 */
const customParser = (value: string): unknown => {
  if (value.includes(',')) return value.split(',')
  return JSON.parse(value)
}

export default customParser
