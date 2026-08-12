import rootRoute from '@src/pages/rootRoute'
import { eventQueryOptions } from '@src/queries/event'
import { createRoute } from '@tanstack/react-router'
import EventPage from './EventPage'
import { eventSchema } from './utils/eventSearchSchema'

export const eventRoute = createRoute({
  path: 'events/$eventId',
  getParentRoute: () => rootRoute,
  loader: ({ context: { queryClient }, params: { eventId } }) =>
    queryClient.ensureQueryData(eventQueryOptions(eventId))
})

export const eventIndexRoute = createRoute({
  path: '/',
  validateSearch: eventSchema,
  getParentRoute: () => eventRoute,
  component: EventPage
})
