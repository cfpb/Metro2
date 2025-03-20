import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type User from 'models/User'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorResults from './EvaluatorResults'
import EvaluatorResultsToggle from './EvaluatorResultsToggle'
import EvaluatorSummary from './EvaluatorSummary'

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
      <EvaluatorSummary
        metadata={evaluatorMetadata}
        user={userData}
        event={eventData}
      />
      <EvaluatorResultsToggle />
      <EvaluatorResults
        evaluatorMetadata={evaluatorMetadata}
        eventData={eventData}
      />
    </>
  )
}
