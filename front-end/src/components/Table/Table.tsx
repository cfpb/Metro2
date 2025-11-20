import { useNavigate, useSearch } from '@tanstack/react-router'
import type { ColDef, ColumnState } from 'ag-grid-community'
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community'
import { AgGridReact } from 'ag-grid-react'
import type { ComponentType, ReactElement } from 'react'
import { useEffect, useRef, useState } from 'react'
import './Table.scss'
import {
  columnDefaults,
  columnTypes,
  generateSortParams,
  gridOptionDefaults,
  parseSortParams
} from './tableUtils'

// Register all Community features
ModuleRegistry.registerModules([AllCommunityModule])

/* Table props
 * height: defaults to 'fixed'
 *   'fixed'
 *      - grid has a set height and is scrollable vertically
 *      - container class sets height to 90% of the viewport's vertical space
 *      - grid's domLayout property is set to 'normal', meaning 'the grid fits the
 *        width and height of the div you provide and scrolls in both directions'
 *   'full'
 *      - grid is the height of its contents
 *      - grid's domLayout property is set to 'autoHeight', meaning 'the grid's height is
 *        set to fit the number of rows so no vertical scrollbar is provided'
 * resizableColumns: defaults to true
 *   true
 *     - all columns get default setting of 'resizable: true', so they can be resized by user
 *     - grid's autoSizeStrategy option is set to 'fitCellContents', which sizes
 *       the columns to fit their content when the first data is rendered in the grid
 *     - grid may scroll horizontally on desktop to accommodate contents
 *   false
 *      - columns get default setting of 'resizable: false', so they can't be resized by user
 *      - no autoSizeStrategy is set on grid -- it fills 100% of available screen width and
 *        columns take width defined in their columnDef
 *      - grid is not horizontally scrollable at desktop screen widths
 * rows: array of generic data objects
 * columnDefinitions: array of AgGrid ColDef objects
 */

interface TableProperties<T> {
  rows: T[]
  columnDefinitions: ColDef[]
  height?: 'fixed' | 'full'
  resizableColumns?: boolean
  NoResultsMessage?: ComponentType
  isLoading?: boolean
  isLoadingError?: boolean
}
export default function Table<T extends object>({
  height = 'fixed',
  resizableColumns = true,
  rows,
  columnDefinitions,
  NoResultsMessage,
  isLoading = false,
  isLoadingError
}: TableProperties<T>): ReactElement {
  // store row data in state
  const [rowData, setRowData] = useState(rows)
  const [initialSortApplied, setInitialSortApplied] = useState(false)
  const gridRef = useRef<AgGridReact<T>>(null)
  const sort: unknown = useSearch({
    strict: false,
    // eslint-disable-next-line @typescript-eslint/no-unsafe-return
    select: search => search.sort
  })

  const navigate = useNavigate()

  const tableHeight = rows.length <= 20 ? 'full' : height

  // Update table when new row data loads
  useEffect(() => {
    setRowData(rows)
  }, [rows])

  /* onDataChanged
   *
   * When the data in the table changes and there's a sort
   * param in the URL, convert the sort param
   * into a column state object and apply it to the table.
   * This will update the sort state of the table (including
   * the sort indicators in the column headers) to reflect the
   * sort params in the URL.
   */
  const onDataChanged = (): void => {
    if (typeof sort === 'string' || Array.isArray(sort)) {
      const sortParams = Array.isArray(sort) ? sort : [sort]
      const sortState = parseSortParams(sortParams) as ColumnState[]
      gridRef.current?.api.applyColumnState({
        state: sortState
      })
    }
  }

  /* onSortChanged
   *
   * When sort changes, check initialSortApplied to see if
   * sort is being applied on initial table load.
   * If so, set initialSortApplied to true.
   *
   * Otherwise, the sort change was triggered by user interaction.
   * Get column data from the table, generate a list of sorted columns,
   * and update the URL params as follows:
   *   - if there are sorted columns, update sort param
   *   - if there are no sorted columns, remove sort param
   *   - reset the page param to 1 so the first page of
   *     the new results is fetched
   */
  const onSortChanged = (): void => {
    if (initialSortApplied) {
      const colState = gridRef.current?.api.getColumnState()
      const sortParams = generateSortParams(colState)
      void navigate({
        to: '.',
        resetScroll: false,
        search: (prev: Record<string, unknown>) => {
          const params = { ...prev }
          if (sortParams) {
            params.sort = sortParams
          } else {
            delete params.sort
          }
          params.page = 1
          return params
        }
      })
    } else {
      setInitialSortApplied(true)
    }
  }

  return (
    <div
      className={`ag-theme-alpine data-grid-container data-grid-container--${tableHeight}-height ${
        NoResultsMessage ? 'data-grid-container--message' : ''
      }`}
      data-testid='data-grid-container'>
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        onGridReady={onDataChanged}
        onSortChanged={onSortChanged}
        onRowDataUpdated={onDataChanged}
        columnDefs={columnDefinitions}
        defaultColDef={{ resizable: resizableColumns, ...columnDefaults }}
        domLayout={tableHeight === 'fixed' ? 'normal' : 'autoHeight'}
        autoSizeStrategy={resizableColumns ? { type: 'fitCellContents' } : undefined}
        columnTypes={columnTypes}
        noRowsOverlayComponent={NoResultsMessage}
        noRowsOverlayComponentParams={{ isError: isLoadingError }}
        // TODO: update to use new Ag-Grid theming approach
        theme='legacy'
        reactiveCustomComponents
        loading={isLoading}
        {...gridOptionDefaults}
      />
    </div>
  )
}
