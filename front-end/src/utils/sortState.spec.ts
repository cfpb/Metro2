import {
  generateColumnStateFromSortArray,
  generateSortArrayFromColumnState,
  validateSortQueryParams
} from './sortState'

describe('generateColumnStateFromSortArray', () => {
  it('returns undefined if there is no sort value', () => {
    expect(generateColumnStateFromSortArray()).toEqual(undefined)
  })

  it('returns array with one column state object when sort array has one item', () => {
    expect(generateColumnStateFromSortArray(['field_name'])).toEqual([
      {
        colId: 'field_name',
        sortIndex: 0,
        sort: 'asc'
      }
    ])
  })

  it('returns a column state object with sort direction', () => {
    expect(generateColumnStateFromSortArray(['-field_name'])).toEqual([
      {
        colId: 'field_name',
        sortIndex: 0,
        sort: 'desc'
      }
    ])
  })

  it('returns a multiple item column state array when sort array has multiple items', () => {
    expect(generateColumnStateFromSortArray(['field_one', '-field_two'])).toEqual([
      {
        colId: 'field_one',
        sortIndex: 0,
        sort: 'asc'
      },
      {
        colId: 'field_two',
        sortIndex: 1,
        sort: 'desc'
      }
    ])
  })
})

describe('generateSortArrayFromColumnState', () => {
  it('returns undefined if there is no column state array', () => {
    expect(generateSortArrayFromColumnState()).toEqual(undefined)
  })

  it('returns undefined if there are no sorted columns', () => {
    expect(
      generateSortArrayFromColumnState([
        {
          colId: 'field_one',
          sortIndex: null,
          sort: null
        },
        {
          colId: 'field_two',
          sortIndex: null,
          sort: null
        }
      ])
    ).toEqual(undefined)
  })

  it('returns array with one item when there is one sorted column', () => {
    expect(
      generateSortArrayFromColumnState([
        {
          colId: 'field_one',
          sortIndex: 0,
          sort: 'asc'
        },
        {
          colId: 'field_two',
          sortIndex: null,
          sort: null
        }
      ])
    ).toEqual(['field_one'])
  })

  it('returns array with one item marked as descending when one descending sorted column', () => {
    expect(
      generateSortArrayFromColumnState([
        {
          colId: 'field_one',
          sortIndex: 0,
          sort: 'desc'
        },
        {
          colId: 'field_two',
          sortIndex: null,
          sort: null
        }
      ])
    ).toEqual(['-field_one'])
  })

  it('returns an array with multiple values when multiple sorted columns', () => {
    expect(
      generateSortArrayFromColumnState([
        {
          colId: 'field_one',
          sortIndex: 0,
          sort: 'desc'
        },
        {
          colId: 'field_two',
          sortIndex: null,
          sort: null
        },
        {
          colId: 'field_three',
          sortIndex: 1,
          sort: 'desc'
        }
      ])
    ).toEqual(['-field_one', '-field_three'])
  })
})

describe('validateSortQueryParams', () => {
  it('returns undefined when no valid values', () => {
    const sort = ['age']
    const validValues = ['name', 'address']
    expect(validateSortQueryParams(sort, validValues)).toEqual(undefined)
  })

  it('removes invalid and returns valid values', () => {
    const sort = ['name', 'age', 'height']
    const validValues = ['name', 'address']
    expect(validateSortQueryParams(sort, validValues)).toEqual(['name'])
  })

  it('removes invalid and returns valid values', () => {
    const sort = ['name', 'address', 'age', 'height']
    const validValues = ['name', 'address']
    expect(validateSortQueryParams(sort, validValues)).toEqual(['name', 'address'])
  })

  it('trims and returns valid values', () => {
    const sort = ['  name', ' address  ']
    const validValues = ['name', 'address']
    expect(validateSortQueryParams(sort, validValues)).toEqual(['name', 'address'])
  })

  it('matches valid values when they have descending prefix', () => {
    const sort = ['-name', 'address', 'age', 'height']
    const validValues = ['name', 'address']
    expect(validateSortQueryParams(sort, validValues)).toEqual(['-name', 'address'])
  })
})
