import type Event from '@src/types/Event'
import fetchData from '@src/utils/fetchData'
import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'

export const fetchEvent = async (eventId: string): Promise<Event> =>
  fetchData<Event>(`/api/events/${eventId}/`, 'event')

export const eventQueryOptions = (
  eventId: string
): UseQueryOptions<Event, Error, Event, string[]> =>
  queryOptions({
    queryKey: ['events', eventId],
    queryFn: async () => fetchEvent(eventId)
  })
