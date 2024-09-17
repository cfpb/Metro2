import { Link } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import Table from 'components/Table/Table'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { COL_DEF_CONSTANTS } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorDownloader from './EvaluatorDownloader'

interface EvaluatorTableData {
  hits: AccountRecord[]
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
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

const getEvaluatorFields = (
  fields_used: string[],
  fields_display: string[]
): string[] => {
  // Create list by combining fields_used and fields_display, each sorted alphabetically,
  // with constant values consumer account number and activity date added at beginning
  const fields = [
    'cons_acct_num',
    'activity_date',
    ...fields_used.sort(),
    ...fields_display.sort()
  ]

  // If php is present, add php1 right after it so they'll be adjacent columns.
  // php1 does not appear in fields metadata lists & the values are not in the data returned by the API --
  // they are generated on the front end when hits data is fetched
  const phpIndex = fields.indexOf('php')
  if (phpIndex > -1) fields.splice(phpIndex + 1, 0, 'php1')

  return fields
}

export default function EvaluatorTable({
  hits,
  evaluatorMetadata,
  eventData
}: EvaluatorTableData): ReactElement {
  // Get list of fields to display for this evaluator
  const fields = getEvaluatorFields(
    evaluatorMetadata.fields_used,
    evaluatorMetadata.fields_display
  )

  // Generate colDefs for this evaluator's fields
  const colDefs = getEvaluatorColDefs(fields, String(eventData.id))

  // Present correct messaging per results in table
  const totalResults = Number(evaluatorMetadata.hits)
  const msg =
    totalResults <= 20
      ? `Showing ${hits.length} out of ${String(evaluatorMetadata.hits)} results`
      : `Showing representative sample of ${hits.length} out of ${String(
          evaluatorMetadata.hits
        )} results`

  return (
    <div className='content-row'>
      <div className='download-row evaluator-hits-row'>
        <h4 className='u-mb0'>{msg}</h4>
        <EvaluatorDownloader
          rows={hits}
          fields={fields}
          eventData={eventData}
          evaluatorId={evaluatorMetadata.id}
        />
      </div>
      <Table rows={hits} columnDefinitions={colDefs} />
    </div>
  )
}
