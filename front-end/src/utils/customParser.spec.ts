import customParser from './customParser'

describe('customParser', () => {
  it('returns comma-separated strings as arrays', () => {
    expect(customParser('1,2,3')).toEqual(['1', '2', '3'])
  })

  it('returns results of JSON.parse() for JSON string', () => {
    expect(customParser('{"key":"value"}')).toEqual({ key: 'value' })
    expect(customParser('"some string"')).toEqual('some string')
  })
})
