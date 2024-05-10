import type { ColDef as ColDefType, ValueFormatterParams } from 'ag-grid-community'
import AnnotatedText from 'components/AnnotatedText'
import type { ReactElement } from 'react'
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
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    valueFormatter: ({ value }: ValueFormatterParams): any => formatNumber(value)
  },
  formattedDate: {
    cellDataType: 'dateString',
    valueFormatter: ({ value }: ValueFormatterParams): string => formatDate(value)
  },
  plainText: {
    cellDataType: 'text'
  },
  currency: {
    cellClass: 'ag-right-aligned-cell',
    cellDataType: 'number',
    headerClass: 'ag-right-aligned-header',
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    valueFormatter: ({ value }: ValueFormatterParams): any => formatUSD(value)
  },
  annotatedText: {
    cellDataType: 'text',
    cellRenderer: ({
      colDef,
      value
    }: {
      colDef: ColDefType
      value: number | string | null | undefined
    }): ReactElement | null => <AnnotatedText field={colDef.field} value={value} />
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
