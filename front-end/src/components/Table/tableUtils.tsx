import type { ValueFormatterParams } from 'ag-grid-community'

const numberFormatter = new Intl.NumberFormat('en', {
  notation: 'standard'
})

// TOOD: consider whether this needs any other type guards
export function formatNumber(val: number | null | undefined): string {
  return val == null ? '' : numberFormatter.format(val) 
}

export const ColumnTypes = {
  wrappableText: { 
    wrapText: true,
    autoHeight: true,
    cellStyle: { wordBreak: 'normal' }
  },
  formattedNumber: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    valueFormatter: ({value}: ValueFormatterParams<any, number | null> ): string => formatNumber(value),
    cellClass: 'ag-right-aligned-cell',
    headerClass: 'ag-right-aligned-header'
  }
}

export const columnDefaults = {
  sortable: true,
  wrapHeaderText: true,
  autoHeaderHeight: true
}

export const gridOptionDefaults = {
  columnTypes: ColumnTypes,
  enableCellTextSelection: true,
  ensureDomOrder: true,
  skipHeaderOnAutoSize: true
}
