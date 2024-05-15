import { Link } from '@tanstack/react-router'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { generateColumnDefinitions, isM2Field } from 'utils/utils'
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

const getEvaluatorFieldsList = (evaluatorMetadata: EvaluatorMetadata): string[] => {
  // Build array of evaluator table columns from fields_used and fields_display lists
  let fields = [
    ...evaluatorMetadata.fields_used,
    ...evaluatorMetadata.fields_display
  ]

  // Add activity date to list of fields since it's a constant & not included in metadata
  fields.unshift('activity_date')

  // If php present in fields, add php1 right after it so they'll be adjacent columns
  const phpIndex = fields.indexOf('php')
  if (phpIndex > -1) {
    fields.splice(phpIndex + 1, 0, 'php1')
  }

  // Filter out anything that's not an M2 field and enforce uniqueness
  // TODO: this is temporary due to extraneous data in the display_fields metadata
  fields = [...new Set(fields)].filter(field => isM2Field(field))
  return fields
}

export default function EvaluatorTable({
  hits,
  evaluatorMetadata
}: EvaluatorTableData): ReactElement {
  // Assemble list of fields for table from metadata
  const fields = getEvaluatorFieldsList(evaluatorMetadata)

  // Generate colDefs for this group of fields
  const colDefs = generateColumnDefinitions(fields)

  // add account number column to colDefs
  colDefs.unshift(accountColDef)

  // also add account number to the fields for download
  fields.unshift('cons_acct_num')

  return (
    <div className='content-row'>
      <div className='download-row'>
        <h4 className='u-mb0'>
          {`Showing ${Math.min(hits.length, 20)} of ${String(
            evaluatorMetadata.hits
          )} results`}
        </h4>
        <EvaluatorDownloader rows={hits} fields={['cons_acct_num', ...fields]} />
      </div>
      <Table rows={hits} columnDefinitions={colDefs} />
    </div>
  )
}
