import { Link } from '@tanstack/react-router'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { annotateData, generateColumnDefinitions, isM2Field } from 'utils/utils'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorDownloader from './EvaluatorDownloader'

interface EvaluatorTableData {
  hits: AccountRecord[]
  evaluatorMetadata: EvaluatorMetadata
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
  evaluatorMetadata
}: EvaluatorTableData): ReactElement {
  const rows = annotateData(hits)

  // Build list of evaluator table columns from the
  // fields_used and fields_display metadata values
  // Filter out anything that's not a M2 field
  // TODO: remove filter
  const fields = [
    ...evaluatorMetadata.fields_used,
    ...evaluatorMetadata.fields_display
  ].filter(field => isM2Field(field))

  // activity_date and cons_acct_num aren't included in the metadata
  // lists of fields because they're returned in every evaluator's results
  // We add them to the start of the fields list here

  fields.unshift('activity_date')

  // Generate colDefs for this group of fields
  const colDefs = generateColumnDefinitions(fields)

  // add account number column to colDefs
  colDefs.unshift(accountColDef)

  return (
    <div className='content-row'>
      <div className='download-row'>
        <h4 className='u-mb0'>
          {`Showing ${Math.min(hits.length, 50)} of ${String(
            evaluatorMetadata.hits
          )} results`}
        </h4>
        <EvaluatorDownloader rows={rows} fields={['cons_acct_num', ...fields]} />
      </div>
      <Table rows={rows} columnDefinitions={colDefs} />
    </div>
  )
}
