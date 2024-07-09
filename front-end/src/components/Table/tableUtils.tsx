import type { ValueFormatterParams } from 'ag-grid-community'
import { formatDate, formatNumber, formatUSD } from 'utils/utils'

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
    headerClass: 'ag-right-aligned-header',
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
    headerClass: 'ag-right-aligned-header',
    // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
    valueFormatter: ({ value }: ValueFormatterParams): string => formatUSD(value),
    minWidth: 130
  }
}

export const columnDefaults = {
  sortable: true,
  wrapHeaderText: true,
  autoHeaderHeight: true,
  // TODO: set widths on each col type
  minWidth: 150
}

export const gridOptionDefaults = {
  enableCellTextSelection: true,
  ensureDomOrder: true,
  skipHeaderOnAutoSize: true
}
