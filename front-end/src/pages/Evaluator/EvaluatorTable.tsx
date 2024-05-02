import { Link } from '@tanstack/react-router'
import Table from 'components/Table/Table'
import { Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { M2_FIELDS } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type EvaluatorMetadata from './Evaluator'

interface EvaluatorTableData {
  hits: AccountRecord[]
  evaluatorMetadata: EvaluatorMetadata
  eventId: number
}

const accountColDef = {
  field: 'cons_acct_num',
  headerName: 'Account number',
  pinned: 'left' as const,
  cellRenderer: ({ value }: { value: string }): ReactElement => (
    <Link
      to='../../accounts/$accountId'
      params={{ accountId: value }}
      className='a-link'>
      {value}
    </Link>
  )
}

export default function EvaluatorTable({
  hits,
  evaluatorMetadata,
  eventId
}: EvaluatorTableData): ReactElement {
  // Get fields from first account activity record in hits
  // TODO: should get the fields from evaluator metadata once available
  const fields = Object.keys(hits[0] || {}).filter(
    i => !['cons_acct_num', 'id'].includes(i)
  )

  // temporarily sort according to M2_FIELDS order
  // this won't be necessary once we get list of fields from evaluator metadata
  fields.sort((a, b) => M2_FIELDS.indexOf(a) - M2_FIELDS.indexOf(b))

  // Generate colDefs for this group of fields
  const colDefs = generateColumnDefinitions(fields)

  // Add account colDef to colDefs
  colDefs.unshift(accountColDef)

  const csvUrl = `/api/events/${eventId}/evaluator/${evaluatorMetadata.id}/csv/`

  return (
    <div className='content-row'>
      <div className='download-row'>
        <h4 className='u-mb0'>
          {`Showing ${Math.min(hits.length, 50)} of ${
            evaluatorMetadata.hits
          } results`}
        </h4>
        <a className='a-btn' href={csvUrl}>
          Download evaluator results
          <span className='a-btn__icon a-btn__icon--on-right'>
            <Icon name='download' />
          </span>
        </a>
      </div>
      <Table rows={hits} columnDefinitions={colDefs} />
    </div>
  )
}
