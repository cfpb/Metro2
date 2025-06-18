import {
  replaceUnderscores,
  titleizeFieldName,
  toSentenceCase
} from './formatStrings'

describe('toSentenceCase', () => {
  it('capitalizes first letter of a string', () => {
    expect(toSentenceCase('this is a string')).toEqual('This is a string')
  })
})

describe('replaceUnderscores', () => {
  it('replaces underscores with spaces', () => {
    expect(replaceUnderscores('string_with_underscores')).toEqual(
      'string with underscores'
    )
  })

  it('trims leading and trailing spaces after replacing underscores', () => {
    expect(replaceUnderscores('__string_with_underscores__')).toEqual(
      'string with underscores'
    )
  })
})

describe('titleizeFieldName', () => {
  it('replaces underscores and capitalizes first letter of string', () => {
    expect(titleizeFieldName('field_name')).toEqual('Field name')
  })
})
