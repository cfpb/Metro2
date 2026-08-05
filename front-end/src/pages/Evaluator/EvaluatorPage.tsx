import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import type EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type Event from '@src/types/Event'
import type User from '@src/types/User'
import { useLoaderData } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import EvaluatorOverview from './overview/EvaluatorOverview'
import EvaluatorResults from './results/EvaluatorResults'

interface EvaluatorPageData {
  evaluatorMetadata: EvaluatorMetadata
  eventData: Event
  userData: User
}

export default function EvaluatorPage(): ReactElement {
  const { evaluatorMetadata, eventData, userData }: EvaluatorPageData =
    useLoaderData({
      from: '/events/$eventId/evaluators/$evaluatorId'
    })
  return (
    <>
      <LocatorBar
        eyebrow='Evaluator'
        heading={evaluatorMetadata.id}
        icon='flag-round'
        breadcrumbs={[
          {
            to: `/events/${String(eventData.id)}`,
            label: 'Back to event results'
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
