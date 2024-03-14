import { createRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import EventPage from './EventPage'

export const eventRoute = createRoute({
  path: 'events/$eventId',
  getParentRoute: () => rootRoute,
})

export const eventIndexRoute = createRoute({
  path: '/',
  getParentRoute: () => eventRoute,
  component: EventPage
})
