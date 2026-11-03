/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
import { formatDate } from '@src/utils/formatDates'
import { formatNumber, formatUSD } from '@src/utils/formatNumbers'
import type { ValueFormatterParams } from 'ag-grid-community'
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
    valueFormatter: ({ value }: ValueFormatterParams): any => formatNumber(value)
  },
  formattedDate: {
    cellDataType: 'dateString',
    valueFormatter: ({ value }: ValueFormatterParams): any => formatDate(value)
  },
  currency: {
    cellClass: 'ag-right-aligned-cell',
    cellDataType: 'number',
    valueFormatter: ({ value }: ValueFormatterParams): any => formatUSD(value)
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
