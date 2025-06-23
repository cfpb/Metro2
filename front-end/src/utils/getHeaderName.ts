import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { titleizeFieldName } from './formatStrings'

/**
 * getHeaderName()
 *
 * Returns a field's title for use in a table or CSV.
 *
 * Tries to get title from header name lookup and falls back to
 * capitalizing the field's name if field not found in lookup.
 *
 * @param {string} field - the name of a field
 * @param {Map<string, string>} lookup - a map of fields & their titles
 * @returns {string} if field is in map:
 *                      title for field from map
 *                   if field is not in map:
 *                      Sentence-case field name with underscores replaced by spaces
 */
const getHeaderName = (
  field: string,
  lookup: Map<string, string> = M2_FIELD_NAMES
): string => lookup.get(field) ?? titleizeFieldName(field)

export default getHeaderName
