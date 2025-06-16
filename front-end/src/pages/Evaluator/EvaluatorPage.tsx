import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'
import type User from 'types/User'
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
