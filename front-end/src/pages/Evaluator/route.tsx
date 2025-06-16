import { createRoute, notFound } from '@tanstack/react-router'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'

import { eventRoute } from 'pages/Event/route'
import { evaluatorHitsQueryOptions } from 'queries/evaluatorHits'
import { eventQueryOptions } from 'queries/event'
import { userQueryOptions } from 'queries/user'
import getEvaluatorDataFromEvent from 'utils/getEvaluatorFromEvent'
import type { z } from 'zod'
import EvaluatorPage from './EvaluatorPage'
import { evaluatorSearchSchema } from './utils/evaluatorSearchSchema'

export async function getEvaluator(
  eventData: Promise<Event>,
  evaluatorId: string
): Promise<EvaluatorMetadata> {
  try {
    const data = await eventData
    const evaluator = getEvaluatorDataFromEvent(data, evaluatorId)
    if (evaluator) return evaluator
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw new Error('404')
  } catch (error) {
    // Throw NotFound error to handle 404s in NotFound component
    // All other errors will be caught by ErrorComponent
    const message = error instanceof Error ? error.message : ''
    if (message === '404') notFound({ throw: true, data: 'evaluator' })
    throw new Error(message)
  }
}

const evaluatorRoute = createRoute({
  path: '/evaluators/$evaluatorId',
  getParentRoute: () => eventRoute,
  shouldReload: false,
  component: EvaluatorPage,
  validateSearch: input =>
    evaluatorSearchSchema.parse(input) as z.input<typeof evaluatorSearchSchema>,
  loader: async ({ context, params: { eventId, evaluatorId } }) => {
    const userData = context.queryClient.ensureQueryData(userQueryOptions())
    const eventData = context.queryClient.ensureQueryData(eventQueryOptions(eventId))
    const evaluatorMetadata = getEvaluator(eventData, evaluatorId)
    void context.queryClient.ensureQueryData(
      evaluatorHitsQueryOptions(eventId, evaluatorId)
    )
    return {
      userData: await userData,
      eventData: await eventData,
      evaluatorMetadata: await evaluatorMetadata
    }
  }
})

export default evaluatorRoute
