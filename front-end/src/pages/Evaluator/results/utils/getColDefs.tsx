import COL_DEF_CONSTANTS from '@src/constants/colDefConstants'
import { Link } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type { ReactElement } from 'react'
import generateColumnDefinitions from 'utils/generateColDefs'

const getEvaluatorColDefs = (fields: string[], eventId: string): ColDef[] => {
  const accountColDef = {
    pinned: 'left' as const,
    cellRenderer: ({ value }: { value: string }): ReactElement => (
      <Link
        to='/events/$eventId/accounts/$accountId'
        params={{ accountId: value, eventId }}
        className='a-link'>
        {value}
      </Link>
    )
  }
  const colDefObj = { ...COL_DEF_CONSTANTS, cons_acct_num: accountColDef }
  // Add default sort to activity date col
  // const activityDateCol = {
  //   ...colDefObj.activity_date,
  //   sort: 'asc',
  //   initialSortIndex: 0
  // }
  // colDefObj.activity_date = activityDateCol
  return generateColumnDefinitions(fields, colDefObj)
}

export default getEvaluatorColDefs
