import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/Evaluator'
import EvaluatorOverview from './overview/EvaluatorOverview'
import EvaluatorResults from './results/EvaluatorResults'

interface EvaluatorPageData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
  userData: User
}

export default function EvaluatorPage(): ReactElement {
  const { eventData, evaluatorMetadata, userData }: EvaluatorPageData =
    useLoaderData({
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
      <EvaluatorOverview
        metadata={evaluatorMetadata}
        user={userData}
        event={eventData}
      />
      <EvaluatorResults
        evaluatorMetadata={evaluatorMetadata}
        eventData={eventData}
      />
    </>
  )
}
