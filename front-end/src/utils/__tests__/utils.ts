import { M2_FIELD_LOOKUPS } from 'node:constants/annotationLookups'
import { annotateAccountRecords, stringifySearchParams } from '../getHeaderName'

import {
  formatDate,
  formatNumber,
  formatUSD,
  getM2Definition
} from 'utils/formatters'

const UNDEFINED = undefined

describe('annotateAccountRecords', () => {
  it('annotates fields with coded values, including arrays', () => {
    const records = [
      {
        id_num: '1601',
        cons_acct_num: '123456789',
        inconsistencies: ['Bankruptcy-DOFD-4', 'Status-DOFD-1'],
        activity_date: '2018-10-31',
        acct_stat: '11',
        amt_past_due: 100,
        current_bal: 100,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '111110010010000000000DDD',
        account_holder__cons_info_ind_assoc: ['A', 'B'],
        terms_freq: 'M'
      }
    ]
    const annotatedRecords = [
      {
        id_num: '1601',
        cons_acct_num: '123456789',
        inconsistencies: ['Bankruptcy-DOFD-4', 'Status-DOFD-1'],
        activity_date: '2018-10-31',
        acct_stat: '11 (0-29 days past the due date (current account))',
        amt_past_due: 100,
        current_bal: 100,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '111110010010000000000DDD',
        account_holder__cons_info_ind_assoc: [
          'A (Petition for Chapter 7 Bankruptcy)',
          'B (Petition for Chapter 11 Bankruptcy)'
        ],
        terms_freq: 'M (Monthly)'
      }
    ]
    expect(annotateAccountRecords(records)).toEqual(annotatedRecords)
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
  // text: January 2024
  // abbreviatedText: Jan 2024
  // default: 01/04/24
  it('returns a text formatted date when passed a date string and format type', () => {
    expect(formatDate('2024-01-23', 'text')).toEqual('January 2024')
    expect(formatDate('2023-11-03', 'text')).toEqual('November 2023')
  })

  it('returns an abbreviated text date when passed a date string and format type', () => {
    expect(formatDate('2024-01-23', 'abbreviatedText')).toEqual('Jan 2024')
    expect(formatDate('2023-11-03', 'abbreviatedText')).toEqual('Nov 2023')
  })

  it('returns a default formatted date when passed a date string', () => {
    expect(formatDate('2024-01-23')).toEqual('01/23/24')
    expect(formatDate('2023-11-03')).toEqual('11/03/23')
  })

  it('returns empty string when passed a non-date-string value', () => {
    expect(formatDate(null)).toEqual('')
    expect(formatDate(UNDEFINED)).toEqual('')
    expect(formatDate('abcdefg')).toEqual('')
    expect(formatDate('11-3-2023')).toEqual('')
  })
})

// describe('formatLongDescription', () => {
//   it('adds H4s to first lines without pseudo code symbols', () => {
//     const str =
//       'This is a header\nSentence\nSentence 2\n\nThis = pseudocode\n\nAnother header'
//     const html: string =
//       '<h4>This is a header</h4>' +
//       '<p>Sentence</p>' +
//       '<p>Sentence 2</p>' +
//       '<p>This = pseudocode</p>' +
//       '<h4>Another header</h4>'
//     expect(formatLongDescription(str)).toEqual(html)
//   })
// })

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
