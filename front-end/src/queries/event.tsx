import type Event from '@src/types/Event'
import fetchData from '@src/utils/fetchData'
import { queryOptions, useSuspenseQuery } from '@tanstack/react-query'

export const fetchEvent = async (eventId: string): Promise<Event> =>
  fetchData<Event>(`/api/events/${eventId}/`, 'event')

export const eventQueryOptions = (eventId: string) =>
  queryOptions({
    queryKey: ['events', eventId],
    queryFn: async () => fetchEvent(eventId)
  })

export const useEventSuspense = (eventId: number | string) => {
  const { data } = useSuspenseQuery(eventQueryOptions(String(eventId)))
  return data
}
