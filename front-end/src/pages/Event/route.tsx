import { createRoute } from '@tanstack/react-router'
import { eventQueryOptions } from 'queries/event'
import rootRoute from '../rootRoute'
import EventPage from './EventPage'

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
