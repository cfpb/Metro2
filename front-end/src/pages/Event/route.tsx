import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { createRoute } from '@tanstack/react-router'
import { evaluatorSegmentMap } from 'utils/constants'
import { fetchData } from 'utils/utils'
import rootRoute from '../rootRoute'
import type Event from './Event'
import EventPage from './EventPage'

export const processEventData = (data: Event): Event => {
  // add temporary categories to event's evaluators by splitting
  // the id into segments and looking up the segment descriptors
  for (const evaluator of data.evaluators) {
    const segments = evaluator.id.split('-')
    segments.pop()
    evaluator.category = segments
      .map(segment => evaluatorSegmentMap.get(segment.toLowerCase()) ?? '')
      .sort()
  }
  return data
}

export const fetchEvent = async (eventId: string): Promise<Event> => {
  const data = await fetchData<Event>(`/api/events/${eventId}/`, 'event')
  return processEventData(data)
}

export const eventQueryOptions = (
  eventId: string
): UseQueryOptions<Event, Error, unknown, string[]> =>
  queryOptions({
    queryKey: ['events', eventId],
    queryFn: async () => fetchEvent(eventId)
  })

export const eventRoute = createRoute({
  path: 'events/$eventId',
  getParentRoute: () => rootRoute,
  loader: async ({ context: { queryClient }, params: { eventId } }) =>
    queryClient.ensureQueryData(eventQueryOptions(eventId))
})

export const eventIndexRoute = createRoute({
  path: '/',
  getParentRoute: () => eventRoute,
  component: EventPage
})
