import type { ReactElement } from 'react'
import { useEffect, useState } from 'react'
import { AgGridReact } from 'ag-grid-react'
import type { ColDef } from 'ag-grid-community';
import { columnDefaults, gridOptionDefaults } from './tableUtils'
import './Table.less'

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
	rows: T[],
	columnDefinitions: ColDef[],
	height?: 'fixed' | 'full',
	resizableColumns?: boolean
}
export default function Table<T extends object>( {
	height='fixed',
	resizableColumns=true,
	rows,
	columnDefinitions
}: TableProperties<T> ): ReactElement {

	// store row data in state
	const [rowData, setRowData] = useState(rows)

	// Update table when new row data loads
	useEffect(() => {
		setRowData(rows)
	}, [rows])

	return (
		<div className="u-mt15 u-mb30">
			<div className={`ag-theme-alpine
			                 data-grid-container
											 data-grid-container--${height}-height`}
					 data-testid='data-grid-container'>
				<AgGridReact rowData={ rowData }
				             columnDefs={ columnDefinitions }
										 defaultColDef={ { resizable: resizableColumns, ...columnDefaults } }
										 domLayout={ height === 'fixed' ? 'normal' : 'autoHeight' }
										 autoSizeStrategy={ resizableColumns ? { type:'fitCellContents' } : undefined }
										 { ...gridOptionDefaults }
										 /> 
			</div>
		</div>
	)
}
