import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { createRoute, defer, notFound } from '@tanstack/react-router'
import type Account from 'pages/Account/Account'
import { fetchData } from 'utils/utils'
import type Event from '../Event/Event'
import { eventQueryOptions, eventRoute } from '../Event/route'
import type EvaluatorMetadata from './Evaluator'
import EvaluatorPage from './EvaluatorPage'

export function getEvaluator(
  eventData: Event,
  evaluatorId: string
): EvaluatorMetadata {
  try {
    const evaluator = eventData.evaluators.find(result => result.id === evaluatorId)
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

export const fetchEvaluatorHits = async (
  eventId: string,
  evaluatorId: string
): Promise<Account[]> => {
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/`
  return fetchData(url, 'hits')
}

export const hitsQueryOptions = (
  eventId: string,
  evaluatorId: string
): UseQueryOptions<Account[], Error, unknown, string[]> =>
  queryOptions({
    queryKey: ['event', eventId, 'evaluator', evaluatorId],
    queryFn: async () => fetchEvaluatorHits(eventId, evaluatorId),
    staleTime: 0
  })

const evaluatorRoute = createRoute({
  path: '/evaluators/$evaluatorId',
  getParentRoute: () => eventRoute,
  component: EvaluatorPage,
  loader: async ({ context: { queryClient }, params: { eventId, evaluatorId } }) => {
    // We don't have to get the evaluator metadata from the API because it will
    // have been included when we fetched the event data on the event parent route.
    // Instead, we ensure that the event data has been received and call getEvaluator
    // to find the evaluator's metadata on the event object.
    const eventData = await queryClient.ensureQueryData(eventQueryOptions(eventId))
    const evaluatorMetadata = getEvaluator(eventData, evaluatorId)
    const evaluatorHits = queryClient.ensureQueryData(
      hitsQueryOptions(eventId, evaluatorId)
    )
    return {
      evaluatorMetadata,
      eventData,
      evaluatorHits: defer(evaluatorHits)
    }
  }
})

export default evaluatorRoute
