import M2_FIELD_NAMES from '../constants/m2FieldNames'
import capitalized from './formatStrings'

// Given a string and a lookup map, returns either the string's value in the lookup
// or, if the string is not found in the lookup, a capitalized version of the string
const getHeaderName = (
  field: string,
  lookup: Map<string, string> = M2_FIELD_NAMES
): string => lookup.get(field) ?? capitalized(field)

export default getHeaderName
