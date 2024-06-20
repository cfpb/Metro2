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

const accountColDef = {
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

const getEvaluatorColDefs = (fields: string[]): ColDef[] => {
  const colDefObj = { ...COL_DEF_CONSTANTS, cons_acct_num: accountColDef }
  return generateColumnDefinitions(fields, colDefObj)
}

const getEvaluatorFields = (
  fields_used: string[],
  record: AccountRecord | null
): string[] => {
  // return empty array if there are no records
  if (!record) return []

  // get list of fields from record and remove id
  const fields = Object.keys(record).filter(item => item !== 'id')

  // sort fields alphabetically and prioritize ones that are used by evaluator
  fields
    .sort()
    .sort(
      (a, b) =>
        (fields_used.indexOf(b as keyof AccountRecord) || 100) -
        (fields_used.indexOf(a as keyof AccountRecord) || 100)
    )

  // If php present, add php1 right after it so they'll be adjacent columns
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
  const fields = getEvaluatorFields(evaluatorMetadata.fields_used, hits[0])

  // Generate colDefs for this evaluator's fields
  const colDefs = getEvaluatorColDefs(fields)

  return (
    <div className='content-row'>
      <div className='download-row'>
        <h4 className='u-mb0'>
          {`Showing ${hits.length} of ${String(evaluatorMetadata.hits)} results`}
        </h4>
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
