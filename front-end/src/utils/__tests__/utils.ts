import getM2CodeDefinition from '../utils'
import { M2_FIELD_LOOKUPS } from '../constants'

describe('getM2CodeDefinition', () => {
  
	it('should return undefined when field has no lookup', () => {
    const definition = getM2CodeDefinition('fake_field', 'fake_value')
		expect(definition).toBeUndefined()
	})

  it('should return undefined when value does not exist on field', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2CodeDefinition(validField, 'fake_value')
		expect(definition).toBeUndefined()
	})

  it('should return undefined when value is null', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2CodeDefinition(validField, null)
		expect(definition).toBeUndefined()
	})

  it('should return undefined when value is undefined', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2CodeDefinition(validField)
		expect(definition).toBeUndefined()
	})

  it('should return definitions for valid fields and values', () => {
    const validFields = Object.keys(M2_FIELD_LOOKUPS)
    for (const field of validFields) {
      const lookup = M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
      const validValues = Object.keys(lookup)
      for (const value of validValues) {
        const definition = getM2CodeDefinition(field, value)
        expect(definition).toEqual(lookup[value as keyof typeof lookup])
      }
    }
	})

})
