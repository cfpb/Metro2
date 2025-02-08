import { Link } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import Table from 'components/Table/Table'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { useMemo } from 'react'
import type { AccountRecord } from 'utils/constants'
import { COL_DEF_CONSTANTS } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'

interface EvaluatorTableData {
  eventData: Event
  data: AccountRecord[]
  fields: string[]
}

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

export default function EvaluatorTable({
  eventData,
  data,
  fields
}: EvaluatorTableData): ReactElement {
  const columnDefinitions = useMemo(
    () => getEvaluatorColDefs(fields, String(eventData.id)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  )
  return <Table rows={data} columnDefinitions={columnDefinitions} />
}
