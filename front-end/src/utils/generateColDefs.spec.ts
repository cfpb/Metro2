import generateColumnDefinitions from './generateColDefs'

describe('generateColumnDefinitions', () => {
  it('returns column definitions for a list of fields', () => {
    const fields = ['acct_stat', 'spc_com_cd']
    const expected = [
      { field: 'acct_stat', headerName: 'Account status' },
      { field: 'spc_com_cd', headerName: 'Special comment code' }
    ]
    expect(generateColumnDefinitions(fields)).toEqual(expected)
  })

  it('adds extra props to a column definition', () => {
    const fields = ['acct_stat', 'spc_com_cd']
    const additionalProps = { acct_stat: { width: 100 } }
    const expected = [
      { field: 'acct_stat', headerName: 'Account status', width: 100 },
      { field: 'spc_com_cd', headerName: 'Special comment code' }
    ]
    expect(generateColumnDefinitions(fields, additionalProps)).toEqual(expected)
  })

  it('generates a sentence-case title for a non-M2 field', () => {
    const fields = ['acct_stat', 'spc_com_cd', 'extra_field']
    const expected = [
      { field: 'acct_stat', headerName: 'Account status' },
      { field: 'spc_com_cd', headerName: 'Special comment code' },
      { field: 'extra_field', headerName: 'Extra field' }
    ]
    expect(generateColumnDefinitions(fields)).toEqual(expected)
  })
})
