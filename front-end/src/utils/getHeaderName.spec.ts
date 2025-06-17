import getHeaderName from './getHeaderName'

const testMap = new Map([
  ['make', 'Manufacturer'],
  ['year', 'Production year']
])

describe('getHeaderName', () => {
  it('returns titles for fields in header lookup', () => {
    expect(getHeaderName('make', testMap)).toEqual('Manufacturer')
    expect(getHeaderName('year', testMap)).toEqual('Production year')
  })

  it('returns sentence-case field name when field is not in header lookup', () => {
    expect(getHeaderName('model', testMap)).toEqual('Model')
    expect(getHeaderName('fuel_type', testMap)).toEqual('Fuel type')
  })

  it('uses M2_FIELD_NAMES as default map', () => {
    expect(getHeaderName('acct_stat')).toEqual('Account status')
    expect(getHeaderName('fake_field')).toEqual('Fake field')
  })
})
