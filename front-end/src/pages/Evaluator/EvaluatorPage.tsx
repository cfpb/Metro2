import type { DeferredPromise } from '@tanstack/react-router'
import { Await, useLoaderData } from '@tanstack/react-router'
import Loader from 'components/Loader/Loader'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { Suspense } from 'react'
import type { AccountRecord } from 'utils/constants'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorSummary from './EvaluatorSummary'
import EvaluatorTable from './EvaluatorTable'

interface EvaluatorPageData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
  userData: User
  evaluatorHits: DeferredPromise<AccountRecord[]>
}

export default function EvaluatorPage(): ReactElement {
  const {
    eventData,
    evaluatorHits,
    evaluatorMetadata,
    userData
  }: EvaluatorPageData = useLoaderData({
    from: '/events/$eventId/evaluators/$evaluatorId'
  })
  return (
    <>
      <LocatorBar
        eyebrow='Inconsistency'
        heading={evaluatorMetadata.id}
        icon='flag-round'
        breadcrumbs={[
          {
            href: `/events/${String(eventData.id)}`,
            text: 'Back to event results'
          }
        ]}
      />
      <EvaluatorSummary
        metadata={evaluatorMetadata}
        user={userData}
        event={eventData}
      />
      <Suspense fallback={<Loader message='Your data is loading' />}>
        <Await promise={evaluatorHits}>
          {(data): ReactElement => (
            <EvaluatorTable
              hits={data}
              evaluatorMetadata={evaluatorMetadata}
              eventData={eventData}
            />
          )}
        </Await>
      </Suspense>
    </>
  )
}
