import type { ValueFormatterParams } from 'ag-grid-community'
import { formatDate, formatUSD } from 'utils/formatDates'
import { formatNumber } from 'utils/formatNumbers'
import suppressKeyboardEvent from './suppressKeyboardEvents'

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
