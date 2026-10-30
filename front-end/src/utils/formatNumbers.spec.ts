import { formatNumber, formatUSD } from './formatNumbers'

const UNDEFINED = undefined

describe('formatNumber', () => {
  it('returns a formatted string when passed a number', () => {
    // underscores used as numeric separators
    expect(formatNumber(123_456_789)).toEqual('123,456,789')
    expect(formatNumber(123)).toEqual('123')
  })

  it('returns a formatted string when passed a numeric value', () => {
    expect(formatNumber('123456789')).toEqual('123,456,789')
    expect(formatNumber('123')).toEqual('123')
  })

  it('returns original value when passed non-numeric value', () => {
    expect(formatNumber(null)).toEqual(null)
    expect(formatNumber(UNDEFINED)).toEqual(UNDEFINED)
    expect(formatNumber('')).toEqual('')
    expect(formatNumber('any string')).toEqual('any string')
  })
})

describe('formatUSD', () => {
  it('returns a formatted string when passed a number', () => {
    // underscores used as numeric separators
    expect(formatUSD(123_456_789)).toEqual('$123,456,789')
    expect(formatUSD(123)).toEqual('$123')
    expect(formatUSD(123.24)).toEqual('$123.24')
    expect(formatUSD(123.2434)).toEqual('$123.24')
  })

  it('returns a formatted string when passed a numeric value', () => {
    expect(formatUSD('123456789')).toEqual('$123,456,789')
    expect(formatUSD('123')).toEqual('$123')
    expect(formatUSD('123.24')).toEqual('$123.24')
    expect(formatUSD('123.2434')).toEqual('$123.24')
  })

  it('returns original value when passed non-numeric value', () => {
    expect(formatUSD(null)).toEqual(null)
    expect(formatUSD(UNDEFINED)).toEqual(UNDEFINED)
    expect(formatUSD('')).toEqual('')
    expect(formatUSD('any string')).toEqual('any string')
  })
})
