import { formatNumber, formatUSD } from './formatNumbers'

const UNDEFINED = undefined

describe('formatNumber', () => {
  it('returns a formatted string when passed a number', () => {
    // underscores used as numeric separators
    expect(formatNumber(123_456_789)).toEqual('123,456,789')
    expect(formatNumber(123)).toEqual('123')
  })

  it('returns empty string when passed non-numeric value', () => {
    expect(formatNumber(null)).toEqual('')
    expect(formatNumber(UNDEFINED)).toEqual('')
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

  it('returns empty string when passed non-numeric value', () => {
    expect(formatUSD(null)).toEqual('')
    expect(formatUSD(UNDEFINED)).toEqual('')
  })
})
