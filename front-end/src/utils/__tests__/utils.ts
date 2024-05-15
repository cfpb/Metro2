import { M2_FIELD_LOOKUPS } from '../constants'
import {
  formatDate,
  formatLongDescription,
  formatNumber,
  formatUSD,
  getM2Definition,
  prepareAccountRecordData
} from '../utils'

describe('prepareAccountRecordData', () => {
  const records = [
    {
      id: 1601,
      inconsistencies: ['Bankruptcy-DOFD-4'],
      activity_date: '2018-10-31',
      amt_past_due: 0,
      current_bal: 0,
      orig_chg_off_amt: 0,
      php: 'DDD001110010010000000000',
      terms_freq: 'M'
    }
  ]

  it('adds and annotates a php1 character', () => {
    const preparedData = prepareAccountRecordData(records)
    const annotatedPHP = `D (No payment history reported/available this month)`
    const preparedRecord = preparedData[0]
    expect('php1' in preparedRecord).toBe(true)
    expect(preparedRecord.php1).toEqual(annotatedPHP)
  })
})

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

describe('formatDate', () => {
  it('returns a formatted string when passed a date string', () => {
    expect(formatDate('2024-01-23')).toEqual('1/23/2024')
    expect(formatDate('2023-11-03')).toEqual('11/3/2023')
  })

  it('returns empty string when passed a non-date-string value', () => {
    expect(formatDate(null)).toEqual('')
    expect(formatDate(UNDEFINED)).toEqual('')
    expect(formatDate('abcdefg')).toEqual('')
    expect(formatDate('11-3-2023')).toEqual('')
  })
})

describe('formatLongDescription', () => {
  it('adds H4s to first lines without pseudo code symbols', () => {
    const str =
      'This is a header\nSentence\nSentence 2\n\nThis = pseudocode\n\nAnother header'
    const html: string =
      '<h4>This is a header</h4>' +
      '<p>Sentence</p>' +
      '<p>Sentence 2</p>' +
      '<p>This = pseudocode</p>' +
      '<h4>Another header</h4>'
    expect(formatLongDescription(str)).toEqual(html)
  })
})

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
