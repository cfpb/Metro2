import type { DeferredPromise } from '@tanstack/react-router'
import { Await, useLoaderData } from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { Suspense } from 'react'
import type { AccountRecord } from 'utils/constants'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorSummary from './EvaluatorSummary'
import EvaluatorTable from './EvaluatorTable'

interface EvaluatorData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
  evaluatorHits: DeferredPromise<{ hits: AccountRecord[] }>
}

export default function EvaluatorPage(): ReactElement {
  const { evaluatorHits, evaluatorMetadata }: EvaluatorData = useLoaderData({
    from: '/events/$eventId/evaluators/$evaluatorId'
  })

  const eventData: Event = useLoaderData({ from: '/events/$eventId' })

  return (
    <>
      <LocatorBar
        eyebrow='Inconsistency'
        heading={evaluatorMetadata.id}
        icon='flag-round'
        breadcrumbs
      />
      <EvaluatorSummary metadata={evaluatorMetadata} />
      <Suspense fallback={<Loader message='Your data is loading' />}>
        <Await promise={evaluatorHits}>
          {(data): ReactElement => (
            <EvaluatorTable
              hits={data.hits}
              evaluatorMetadata={evaluatorMetadata}
              eventData={eventData}
            />
          )}
        </Await>
      </Suspense>
    </>
  )
}
