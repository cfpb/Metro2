/**
 * sentenceCase()
 *
 * Capitalizes first letter of string.
 *
 * @param {string} str - a string
 * @returns {string} - String with first letter capitalized
 */
export const toSentenceCase = (str: string): string =>
  `${str[0].toUpperCase()}${str.slice(1)}`

/**
 * replaceUnderscores()
 *
 * Replaces underscores with spaces and strips leading / trailing blank space.
 *
 * @param {string} str - a string
 * @returns {string} - String with underscores replaced by spaces
 */
export const replaceUnderscores = (str: string): string =>
  str.replaceAll('_', ' ').trim()

/**
 * titleizeFieldName()
 *
 * Removes underscores from string and capitalizes first letter
 *
 * @param {string} str - a string
 * @returns {string} - Capitalized string without underscores
 */
export const titleizeFieldName = (str: string): string =>
  toSentenceCase(replaceUnderscores(str))
