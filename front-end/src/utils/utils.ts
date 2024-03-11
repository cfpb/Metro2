import { M2_FIELD_LOOKUPS } from './constants'

/**
 * Takes an id and value for a Metro2 field,
 * accesses the lookup for the field's code definitions,
 * and returns either the definition corresponding with
 * the value provided for the field or undefined.
 */
export default function getM2CodeDefinition( 
  fieldId: string,
  fieldValue?: number | string | null
): string | undefined {
  if (fieldValue != null && fieldId in M2_FIELD_LOOKUPS) {
    const lookup = M2_FIELD_LOOKUPS[fieldId as keyof typeof M2_FIELD_LOOKUPS]
    if (fieldValue in lookup) {
      return lookup[fieldValue as keyof typeof lookup]
    }
  }
  return undefined
}
