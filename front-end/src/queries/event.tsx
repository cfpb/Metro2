import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import type Event from 'types/Event'
import fetchData from 'utils/fetchData'

export const fetchEvent = async (eventId: string): Promise<Event> =>
  fetchData<Event>(`/api/events/${eventId}/`, 'event')

export const eventQueryOptions = (
  eventId: string
): UseQueryOptions<Event, Error, Event, string[]> =>
  queryOptions({
    queryKey: ['events', eventId],
    queryFn: async () => fetchEvent(eventId)
  })
