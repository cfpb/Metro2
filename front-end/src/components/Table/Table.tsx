import {
  generateColumnStateFromSortArray,
  generateSortArrayFromColumnState
} from '@src/utils/sortState'
import { useNavigate, useSearch } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community'
import { AgGridReact } from 'ag-grid-react'
import type { ComponentType, ReactElement } from 'react'
import { useEffect, useRef, useState } from 'react'
import './Table.scss'
import { columnDefaults, columnTypes, gridOptionDefaults } from './tableUtils'
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
  defaultSort: string[]
}

export default function Table<T extends object>({
  height = 'fixed',
  resizableColumns = true,
  rows,
  columnDefinitions,
  NoResultsMessage,
  isLoading = false,
  isLoadingError,
  defaultSort
}: TableProperties<T>): ReactElement {
  // store row data in state
  const [rowData, setRowData] = useState(rows)
  const gridRef = useRef<AgGridReact<T>>(null)

  const tableHeight = rows.length <= 20 ? 'full' : height

  const navigate = useNavigate()

  const sort = useSearch({
    strict: false,
    select: search => search.sort ?? defaultSort
  })

  // Update table when new row data loads
  useEffect(() => {
    setRowData(rows)
  }, [rows])

  /* onDataChanged
   *
   * When new data is loaded in the table,
   * apply sort params from the URL & clear any other sorting
   * to ensure the sort state in the table matches the sort state in the URL.
   *
   */
  const onDataChanged = (): void => {
    gridRef.current?.api.applyColumnState({
      state: generateColumnStateFromSortArray(sort),
      defaultState: { sort: null } // clear any other sort state in the table
    })
  }

  /* onSortChanged
   *
   * Handle updates to column sort state.
   * 1. If sort has been removed, restore default sort.
   * 2. If sort has changed, navigate with new sort params.
   *
   */
  const onSortChanged = (): void => {
    // Generate a list of the currently sorted columns.
    const columnState = gridRef.current?.api.getColumnState()
    let currentSort = generateSortArrayFromColumnState(columnState)

    // If the current sort state matches the URL sort state,
    // onSortChanged was triggered programmatically when sorting was applied
    // in onDataChanged, so we don't need to do anything.
    if (JSON.stringify(currentSort) === JSON.stringify(sort)) return

    // If there aren't any sorted columns, use the default sort array instead.
    // Update column state to show default sort in the table because navigating
    //
    if (currentSort === undefined) {
      gridRef.current?.api.applyColumnState({
        state: generateColumnStateFromSortArray(defaultSort)
      })
      currentSort = defaultSort
    }

    // Navigate to the current page with the new sort params.
    // If data is paginated, reset to page 1 because we always
    // want to show the first page of a new set of results.
    if (JSON.stringify(currentSort) !== JSON.stringify(sort)) {
      void navigate({
        to: '.',
        resetScroll: false,
        search: (prev: Record<string, unknown>) => {
          const newSearch = { ...prev, sort: currentSort }
          if ('page' in newSearch) {
            newSearch.page = 1
          }
          return newSearch
        }
      })
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
        onSortChanged={onSortChanged}
        onRowDataUpdated={onDataChanged}
        columnDefs={columnDefinitions}
        defaultColDef={{ resizable: resizableColumns, ...columnDefaults }}
        domLayout={tableHeight === 'fixed' ? 'normal' : 'autoHeight'}
        autoSizeStrategy={resizableColumns ? { type: 'fitCellContents' } : undefined}
        columnTypes={columnTypes}
        noRowsOverlayComponent={NoResultsMessage}
        noRowsOverlayComponentParams={{ isError: isLoadingError }}
        // Update to use new Ag-Grid theming approach
        theme='legacy'
        loading={isLoading}
        {...gridOptionDefaults}
      />
    </div>
  )
}
