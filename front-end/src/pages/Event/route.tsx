import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { createRoute } from '@tanstack/react-router'
import { fetchData } from 'utils/utils'
import rootRoute from '../rootRoute'
import type Event from './Event'
import EventPage from './EventPage'

export const fetchEvent = async (eventId: string): Promise<Event> =>
  fetchData<Event>(`/api/events/${eventId}/`, 'event')

export const eventQueryOptions = (
  eventId: string
): UseQueryOptions<Event, Error, Event, string[]> =>
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
