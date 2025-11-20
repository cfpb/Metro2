import type { ColumnState, ValueFormatterParams } from 'ag-grid-community'
import { formatDate } from 'utils/formatDates'
import { formatNumber, formatUSD } from 'utils/formatNumbers'
import suppressKeyboardEvent from './suppressKeyboardEvents'

/**
 *
 * Takes an array of AgGrid columnState objects with format
 *
 *    {
 *       sort: 'asc' | 'desc' | null,
 *       sortIndex: number,
 *       colId: string,
 *       ...
 *    }
 *
 * and returns an array of strings with format
 *
 * `{-}columnId`
 *
 * that are ordered by sortIndex.
 *
 * @param {array} columnStateArray - array of ag-grid columnState objects
 * @returns {array | null} If there are sorted columns, returns an ordered array of sort strings.
 *                         Otherwise, returns null.
 */
export const generateSortParams = (
  columnStateArray: ColumnState[] | undefined
): string[] | null => {
  if (columnStateArray) {
    // filter non-sorted columns out, sort the remainder by sortIndex,
    // and return an array of `{-}colId` strings
    return columnStateArray
      .filter(col => col.sort != null)
      .sort((colA, colB) => (colA.sortIndex ?? 0) - (colB.sortIndex ?? 0))
      .map(col => (col.sort === 'desc' ? `-${col.colId}` : col.colId))
  }
  return null
}

/**
 *
 * Takes an array of strings with format
 *
 * `{-}columnId`
 *
 * that are ordered by sortIndex and returns an array of
 * AgGrid columnState objects with format
 *
 *    {
 *       sort: 'asc' | 'desc' | null,
 *       sortIndex: number,
 *       colId: string,
 *       ...
 *    }
 *
 * @param {array | null} sortParams - An array of sort strings or null
 * @returns {array} - array of AgGrid columnState objects
 *
 */
export const parseSortParams = (sortParams: string[] | null): object[] | null => {
  if (!sortParams) return null
  return [...sortParams].map((item, index) => {
    const descending = item.startsWith('-')
    return {
      colId: descending ? item.slice(1) : item,
      sortIndex: index,
      sort: descending ? 'desc' : 'asc'
    }
  })
}

export const removeSortParams = (cols: object[]): object[] =>
  cols.map(col => {
    if ('sort' in col || 'sortOrder' in col) {
      const unsortedCol = { ...col }
      if ('sort' in unsortedCol) delete unsortedCol.sort
      if ('sortOrder' in unsortedCol) delete unsortedCol.sortOrder
      return unsortedCol
    }
    return col
  })

/**
 *
 * Takes an unknown sort param value and filters out anything that is not
 * a string with format `{-}columnId`.
 *
 * Returns either an array of such strings or null.
 *
 * @param {unknown} sortParams - An unknown value
 * @returns {array | null} - array of valid strings or null
 *
 */
export const validateSortParams = (
  sortParams: unknown,
  validKeys: (number | string)[]
): string[] | null => {
  const validValues = []
  const arr = Array.isArray(sortParams) ? sortParams : [sortParams]
  for (const item of arr) {
    const trimmed = String(item).trim()
    const value = trimmed.startsWith('-') ? trimmed.slice(1) : trimmed
    if (validKeys.includes(value)) validValues.push(trimmed)
  }
  return validValues.length > 0 ? validValues : null
}

export const columnTypes = {
  wrappableText: {
    wrapText: true,
    autoHeight: true,
    cellStyle: { wordBreak: 'normal' },
    cellDataType: 'text'
  },
  formattedNumber: {
    cellClass: 'ag-right-aligned-cell',
    cellDataType: 'number',
    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
    valueFormatter: ({ value }: ValueFormatterParams): string => formatNumber(value)
  },
  formattedDate: {
    cellDataType: 'dateString',
    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
    valueFormatter: ({ value }: ValueFormatterParams): string => formatDate(value)
  },
  plainText: {
    cellDataType: 'text'
  },
  currency: {
    cellClass: 'ag-right-aligned-cell',
    cellDataType: 'number',
    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
    valueFormatter: ({ value }: ValueFormatterParams): string => formatUSD(value)
  }
}

export const columnDefaults = {
  sortable: true,
  wrapHeaderText: true,
  autoHeaderHeight: true,
  minWidth: 150,
  suppressKeyboardEvent,
  unSortIcon: true
}

export const gridOptionDefaults = {
  enableCellTextSelection: true,
  ensureDomOrder: true,
  skipHeaderOnAutoSize: true,
  suppressColumnVirtualisation: true,
  suppressRowVirtualisation: true,
  showNoRowsOverlay: true,
  alwaysShowHorizontalScroll: true,
  suppressRowTransform: true
}
