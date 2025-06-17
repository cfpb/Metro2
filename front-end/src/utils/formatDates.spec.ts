import { formatDate, formatDateRange, isDateString } from './formatDates'

const UNDEFINED = undefined

describe('isDateString', () => {
  it('returns true if input is a date string', () => {
    expect(isDateString('2024-01-23')).toEqual(true)
    expect(isDateString('11-3-2023')).toEqual(true)
    expect(isDateString('January 3, 2023')).toEqual(true)
  })

  it('returns false when input is not a date string', () => {
    expect(isDateString(null)).toEqual(false)
    expect(isDateString(UNDEFINED)).toEqual(false)
    expect(isDateString('abcdefg')).toEqual(false)
  })
})

describe('formatDate', () => {
  it('returns a default formatted date when passed a date string', () => {
    expect(formatDate('2023-11-03')).toEqual('11/03/23')
    expect(formatDate('11-3-2023')).toEqual('11/03/23')
    expect(formatDate('January 3, 2023')).toEqual('01/03/23')
  })

  it('returns a text formatted date when passed a date string and format type', () => {
    expect(formatDate('2024-01-23', 'text')).toEqual('Jan 2024')
  })

  it('returns empty string when passed a non-date-string value', () => {
    expect(formatDate(null)).toEqual('')
    expect(formatDate(UNDEFINED)).toEqual('')
    expect(formatDate('abcdefg')).toEqual('')
  })
})

describe('formatDateRange', () => {
  it('returns a default formatted date range when passed start and end date strings', () => {
    expect(formatDateRange('2024-01-23', '2024-02-23')).toEqual(
      '01/23/24 - 02/23/24'
    )
    expect(formatDateRange('January 23, 2024', 'February 23, 2024')).toEqual(
      '01/23/24 - 02/23/24'
    )

    expect(formatDateRange('01/23/2024', '02/23/2024')).toEqual(
      '01/23/24 - 02/23/24'
    )
  })

  it('returns an text formatted date range when passed start and end date strings', () => {
    expect(formatDateRange('2024-01-23', '2024-02-23', 'text')).toEqual(
      'Jan 2024 - Feb 2024'
    )
  })

  it('returns empty string when passed one or more invalid params', () => {
    expect(formatDateRange('2023-01-23', null)).toEqual('')
    expect(formatDateRange('string one', 'string two')).toEqual('')
  })
})
