import { formatDate } from 'utils/formatDates'

const UNDEFINED = undefined

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
