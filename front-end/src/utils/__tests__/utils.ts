import { M2_FIELD_LOOKUPS } from '../constants'
import {
  annotateValue,
  formatDate,
  formatLongDescription,
  formatNumber,
  formatUSD,
  getM2Definition,
  prepareAccountRecordData
} from '../utils'

const UNDEFINED = undefined

const records = [
  {
    id_num: '1601',
    cons_acct_num: '123456789',
    inconsistencies: ['Bankruptcy-DOFD-4', 'Status-DOFD-1'],
    activity_date: '2018-10-31',
    acct_stat: '1',
    amt_past_due: 100,
    current_bal: 100,
    orig_chg_off_amt: 0,
    dofd: '2018-01-31',
    php: '111110010010000000000DDD',
    account_holder__cons_info_ind_assoc: ['A', 'B'],
    terms_freq: 'M'
  },
  {
    id_num: '3983',
    cons_acct_num: '987654321',
    inconsistencies: ['Status-DOFD-1'],
    activity_date: '2018-10-31',
    acct_stat: '2',
    amt_past_due: 690,
    current_bal: 690,
    orig_chg_off_amt: 0,
    dofd: '2018-05-31',
    php: '111100000000000000000DDD',
    account_holder__cons_info_ind_assoc: [],
    terms_freq: 'M'
  }
]

describe('prepareAccountRecordData', () => {
  it('adds and annotates a php1 character', () => {
    const record = records[0]

    // when the first record includes php, php1 should be generated
    expect('php1' in record).toBe(false)
    const preparedData = prepareAccountRecordData(records)
    const preparedRecord = preparedData[0]
    expect('php1' in preparedRecord).toBe(true)

    // the php1 value should start with the first character of the php
    expect(preparedRecord.php1?.startsWith(record.php[0])).toBe(true)

    // the php1 value should be annotated
    expect(preparedRecord.php1).toEqual(annotateValue('php1', record.php[0]))
  })

  it('only adds php1 if php present', () => {
    const preparedData = prepareAccountRecordData([
      {
        cons_acct_num: '12345'
      }
    ])

    // records without php values should not get a php1
    expect('php1' in preparedData[0]).toBe(false)
  })
})

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
    expect(formatDate('2024-01-23')).toEqual('01/23/24')
    expect(formatDate('2023-11-03')).toEqual('11/03/23')
  })

  it('returns a shorthand date when passed a date string and flag', () => {
    expect(formatDate('2024-01-23', true)).toEqual('Jan 2024')
    expect(formatDate('2023-11-03', true)).toEqual('Nov 2023')
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
