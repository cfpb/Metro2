import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { filterableFields, getTableFields, identifierFields } from './getTableFields'

describe('getTableFields', () => {
  it('should return fields in correct order', () => {
    const fieldsUsed = ['acct_type', 'port_type']

    const result = getTableFields(fieldsUsed)

    // The first two fields should be the identifier fields
    expect(result.slice(0, 2)).toEqual(identifierFields)

    // The fields used should come next
    expect(result.slice(2, 4)).toEqual(fieldsUsed)

    // Then the filterable fields
    expect(result.slice(4, 18)).toEqual(filterableFields)

    // Then the remaining M2 fields, in order, with the
    // above fields filtered out
    const remainingFields = [...M2_FIELD_NAMES.keys()].filter(
      value =>
        ![...identifierFields, ...fieldsUsed, ...filterableFields].includes(value)
    )
    expect(result.slice(18)).toEqual(remainingFields)
  })
})
