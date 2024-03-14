import { formatNumber } from '../Table/tableUtils'

describe('formatNumber', () => {
	it('returns a formatted string when passed a number', () => {
    const formatttedLongNumber = formatNumber(123456789)
    expect(formatttedLongNumber).toEqual('123,456,789')

    const formattedShortNumber = formatNumber(123)
    expect(formattedShortNumber).toEqual('123')
	})

  it('returns an empty string when passed null or undefined', () => {
    const formattedNullValue = formatNumber(null)
    expect(formattedNullValue).toBe('')

    const formattedUndefinedValue = formatNumber(undefined)
    expect(formattedUndefinedValue).toBe('')
	})
})
