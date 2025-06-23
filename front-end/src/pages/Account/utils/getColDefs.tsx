import COL_DEF_CONSTANTS from '@src/constants/colDefConstants'
import type { ColDef } from 'ag-grid-community'
import type { ReactElement } from 'react'
import generateColumnDefinitions from 'utils/generateColDefs'

// Generate a column definition for the inconsistencies column
// Pass the inconsistencies legend for this account in cellRendererParams
// In cellRenderer, replace evaluator ids in the record's inconsistencies list
// with their index in the legend
export const getInconsistenciesColDef = (
  accountInconsistencies: string[]
): object => ({
  cellRendererParams: { accountInconsistencies },
  cellDataType: false,
  cellRenderer: ({ value }: { value: [] }): ReactElement => (
    <>{value.map(item => accountInconsistencies.indexOf(item) + 1).join(', ')}</>
  ),
  minWidth: 175
})

export const getColDefs = (
  fields: string[],
  inconsistencies: string[]
): ColDef[] => {
  const colDefProps = {
    ...COL_DEF_CONSTANTS,
    inconsistencies: getInconsistenciesColDef(inconsistencies),
    activity_date: { pinned: 'left', type: 'formattedDate', minWidth: 160 }
  }
  return generateColumnDefinitions(fields, colDefProps)
}
