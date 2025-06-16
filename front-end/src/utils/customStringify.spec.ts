import { stringifySearchParams } from './customStringify'

describe('stringifySearchParams', () => {
  it('returns empty string for empty or null objects', () => {
    expect(stringifySearchParams({})).toEqual('')
    expect(stringifySearchParams(null)).toEqual('')
  })

  it('removes blank params', () => {
    expect(stringifySearchParams({ test: '' })).toEqual('')
  })

  it('handles numbers and strings', () => {
    const obj = {
      third: 'three',
      first: 'one',
      second: '2'
    }
    expect(stringifySearchParams(obj)).toEqual('?first=one&second=2&third=three')
  })

  it('sorts params', () => {
    const obj = {
      third: 'three',
      first: 'one',
      second: 'two'
    }
    expect(stringifySearchParams(obj)).toEqual('?first=one&second=two&third=three')
  })
})
