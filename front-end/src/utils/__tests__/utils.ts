import { M2_FIELD_LOOKUPS } from '../constants'
import { getM2Definition } from '../utils'

describe('getM2Definition', () => {
  it('should return undefined when field has no lookup', () => {
    const definition = getM2Definition('fake_field', 'fake_value')
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value does not exist on field', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField, 'fake_value')
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value is null', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField, null)
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value is undefined', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField)
    expect(definition).toBeUndefined()
  })

  it('should return definitions for valid fields and values', () => {
    const validFields = Object.keys(M2_FIELD_LOOKUPS)
    for (const field of validFields) {
      const lookup = M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
      const validValues = Object.keys(lookup)
      for (const value of validValues) {
        const definition = getM2Definition(field, value)
        expect(definition).toEqual(lookup[value as keyof typeof lookup])
      }
    }
  })
})
