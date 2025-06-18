import { customStringify, stringifySearchParams } from './customStringify'

const UNDEFINED = undefined

describe('customStringify', () => {
  it('returns trimmed strings', () => {
    expect(customStringify('this is a string')).toEqual('this is a string')
    expect(customStringify('  string with spaces  ')).toEqual('string with spaces')
  })

  it('returns numbers converted to strings', () => {
    expect(customStringify(24)).toEqual('24')
  })

  it('returns arrays as sorted, comma-separated strings', () => {
    expect(customStringify(['red', 'blue', 'green'])).toEqual('blue,green,red')
    expect(customStringify([3, 1, 2])).toEqual('1,2,3')
    expect(customStringify(['red', 'blue', 3, 1])).toEqual('1,3,blue,red')
  })

  it('returns JSON.stringified objects', () => {
    expect(customStringify({ color: 'red', border: 'green' })).toEqual(
      '{"color":"red","border":"green"}'
    )
  })

  it('returns empty string for empty, null, or undefined values', () => {
    expect(customStringify(null)).toEqual('')
    expect(customStringify(UNDEFINED)).toEqual('')
    expect(customStringify('    ')).toEqual('')
    expect(customStringify('')).toEqual('')
  })
})

describe('stringifySearchParams', () => {
  it('returns empty string for empty or null objects', () => {
    expect(stringifySearchParams({})).toEqual('')
    expect(stringifySearchParams(null)).toEqual('')
    expect(stringifySearchParams(UNDEFINED)).toEqual('')
  })

  it('removes blank params', () => {
    const params = { blank: '  ', has_value: 'value' }
    expect(stringifySearchParams(params)).toEqual('?has_value=value')
  })

  it('stringifies search params containing numbers and strings', () => {
    const params = {
      first: 'one',
      second: 2
    }
    expect(stringifySearchParams(params)).toEqual('?first=one&second=2')
  })

  it('sorts params', () => {
    const params = {
      third: 'three',
      first: 'one',
      second: 'two'
    }
    expect(stringifySearchParams(params)).toEqual(
      '?first=one&second=two&third=three'
    )
  })

  it('sorts and comma-separates arrays', () => {
    const params = {
      selected: [2, 1, 3]
    }
    expect(stringifySearchParams(params)).toEqual('?selected=1,2,3')
  })
})
