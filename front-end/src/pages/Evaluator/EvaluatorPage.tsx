import type { DeferredPromise } from '@tanstack/react-router'
import { Link, useAwaited, useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorSummary from './EvaluatorSummary'

interface EvaluatorData {
  evaluatorMetadata: EvaluatorMetadata
  evaluatorHits: DeferredPromise<{ hits: AccountRecord[] }>
}

const accountColDef = {
  field: 'cons_acct_num',
  headerName: 'Account number',
  pinned: 'left' as const,
  cellRenderer: ({ value }: { value: string }): ReactElement => (
    <Link to='../../accounts/$accountId' params={{ accountId: value }}>
      {value}
    </Link>
  )
}

export default function EvaluatorPage(): ReactElement {
  const { evaluatorHits, evaluatorMetadata }: EvaluatorData = useLoaderData({
    from: '/events/$eventId/evaluators/$evaluatorId'
  })
  const data = useAwaited({ promise: evaluatorHits })

  const awaitedData = data[0]
  const { hits } = awaitedData

  // Get fields from first account activity record in hits
  // TODO: should get the fields from evaluator metadata once available
  const fields = Object.keys(hits[0] || {})

  // Generate colDefs for this group of fields
  const colDefs = generateColumnDefinitions(fields)

  // Add account colDef to colDefs
  colDefs.unshift(accountColDef)

  return (
    <>
      <LocatorBar
        eyebrow='Inconsistency'
        heading={evaluatorMetadata.name || evaluatorMetadata.id}
        breadcrumbs
      />
      <EvaluatorSummary metadata={evaluatorMetadata} />
      <Table rows={hits} columnDefinitions={colDefs} />
    </>
  )
}
