import type { ColumnState } from 'ag-grid-community'

/**
 * The Metro 2 tool table component and API support sorting by
 * multiple fields at the same time.
 *
 * The multisort lifecycle (mainly relevant to the evaluator page,
 * where sorting is done on the server)
 *
 * Within the tool, sort state is converted between three formats:
 *   - in the URL, sort state is stored as a string containing
 *     one or more field names, separated by commas and
 *     prefixed by '-' for descending sort:
 *
 *        'sort=field_one' OR
 *        'sort=field_one,-field_two'
 *
 *   - In the router, sort state is stored as an array
 *     of field names, prefixed by '-' for descending sort:
 *
 *        ['field_one] OR
 *.       ['field_one', '-field_two']
 *
 *   - In Ag Grid tables, sort state is stored in column objects:
 *
 *        [{
 *          sort: 'asc', // null if no sort applied
 *          sortIndex: 0,
 *          colId: 'field_one',
 *          ...
 *        }, {
 *          sort: 'desc', // null if no sort applied
 *          sortIndex: 1,
 *          colId: 'field_two',
 *          ...
 *        }]
 *
 *
 * Sorting a table
 *
 * When a user updates sorting on a table, the Table component
 * accesses the current column state and passes it
 * to the function provided in the `sortHandler` prop.
 *
 * In the sortHandler, the 'generateSortArrayFromColumnState' function
 * can be used to convert the table's sort state into an array
 * that can be passed to the router's navigate function.
 *
 * On navigation, the router will generate a new URL with updated
 * querystring, using `customStringify` to convert the sort array
 * into a single string with commas separating the array values.
 *
 *
 * Loading a page with a sort parameter in the URL
 *
 * When the router loads a page with a sort param in the querystring, it
 * uses the `customParser` function to convert the sort param into an array
 * if it contains commas.
 *
 * Validation should be configured on routes where a sort param is expected
 * using the `validateSortQueryParams` function to screen out any values
 * from the sort array that aren't in a whitelist of field names.
 *
 * The data passed to the table has already been sorted on the server,
 * but we need to show which columns are sorted in the table component's header.
 * To do so, we can use the router's `useSearch` hook to get the validated sort array,
 * convert it into a column state object with `generateColumnStateFromSortArray`,
 * and then pass it to the table via the `columnState` prop.
 *
 */

/**
 * generateColumnStateFromSortArray
 *
 * Takes the sort value parsed from the query string and validated using
 * the validateSortQueryParams function. This value should be:
 *  - undefined (if there is no sort value in the query string, or if
 *    the sort value has not passed validation), OR
 *  - an array of valid sort fields returned from validateSortQueryParams,
 *    in sort order, prefixed by '-' when sort is descending, ie:
 *.     ['field_name', '-field_name_two']
 *
 * If sort value is a valid array of fields,
 * returns an array of AgGrid columnState objects with format:
 *
 *    {
 *       sort: 'asc' | 'desc' ('desc' if field name prefixed by '-', 'asc' otherwise),
 *       sortIndex: number (index in query param array),
 *       colId: string (field_name)
 *    }
 *
 * @param {array | undefined} sortQueryParams - Array of sort query params
 * @returns {array} - Array of AgGrid columnState objects
 *
 */
export const generateColumnStateFromSortArray = (
  sortQueryParams?: string[]
): ColumnState[] | undefined => {
  if (Array.isArray(sortQueryParams)) {
    return [...sortQueryParams].map((item, index) => {
      const descending = item.startsWith('-')
      return {
        colId: descending ? item.slice(1) : item,
        sortIndex: index,
        sort: descending ? 'desc' : 'asc'
      }
    })
  }
}

/**
 * generateSortArrayFromColumnState
 *
 * Takes an array of AgGrid columnState objects with format:
 *
 *    {
 *       sort: 'asc' | 'desc' | null,
 *       sortIndex: number,
 *       colId: string,
 *       ...
 *    }
 *
 * and returns an array of colId strings, ordered by sortIndex and
 * prefixed by '-' if sort is 'desc':
 *
 * ['col_id', '-col_id_two']
 *
 *
 * @param {array} columnStateArray - array of ag-grid columnState objects
 * @returns {array | undefined} If there are sorted columns,
 *                              returns an ordered array of sort strings.
 *                              Otherwise, returns undefined.
 */
export const generateSortArrayFromColumnState = (
  columnStateArray?: ColumnState[]
): string[] | undefined => {
  if (columnStateArray) {
    // Filter non-sorted columns out,
    // sort the remainder by sortIndex,
    // and return an array of `{-}colId` strings
    const sortArray = columnStateArray
      .filter(col => col.sort != null)
      .toSorted((colA, colB) => (colA.sortIndex ?? 0) - (colB.sortIndex ?? 0))
      .map(col => (col.sort === 'desc' ? `-${col.colId}` : col.colId))
    return sortArray.length > 0 ? sortArray : undefined
  }
}

/**
 * validateSortQueryParams
 *
 * Validates sort query params that have been parsed from
 * querystring using the `customParser` function.
 *
 * A valid multisort querystring param would contain one or more
 * valid field names, prefixed by '-' for descending sort:
 *
 * 'sort=field_one' OR
 * 'sort=field_one,-field_two'
 *
 * After parsing, which separates strings containing commas into arrays,
 * a valid sort value would be either a string containing a single valid field name
 * or an array of valid field names, with or without a '-' prefix:
 *
 * 'field_one' OR
 * ['field_one', '-field_two']
 *
 * This function takes whatever sort value was parsed from the querystring
 * and a list of valid fields, filters out anything that is not in the valid
 * field list, and returns either an array of valid sortable field names
 * or undefined.
 *
 * @param {unknown} sortQueryStringVal - An unknown value
 * @returns {array | undefined} - array of valid strings or undefined
 *
 */
export const validateSortQueryParams = (
  sortQueryStringVal: unknown,
  validKeys: (number | string)[]
): string[] | undefined => {
  const validValues = []
  const arr = Array.isArray(sortQueryStringVal)
    ? sortQueryStringVal
    : [sortQueryStringVal]
  for (const item of arr) {
    const trimmed = String(item).trim()
    const value = trimmed.startsWith('-') ? trimmed.slice(1) : trimmed
    if (validKeys.includes(value)) validValues.push(trimmed)
  }
  return validValues.length > 0 ? validValues : undefined
}
