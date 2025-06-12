import { Link } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import type { ReactElement } from 'react'
import generateColumnDefinitions from 'utils/generateColDefs'
import COL_DEF_CONSTANTS from '../../../../constants/colDefConstants'

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
  return generateColumnDefinitions(fields, colDefObj)
}

export default getEvaluatorColDefs
