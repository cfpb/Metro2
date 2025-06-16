import capitalized from './formatStrings'

describe('capitalized', () => {
  it('capitalizes first letter of a string', () => {
    expect(capitalized('this is a string')).toEqual('This is a string')
  })
})
