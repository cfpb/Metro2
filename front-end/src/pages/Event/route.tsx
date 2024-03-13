import type { ReactElement } from 'react';
import { createRoute, Outlet } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import EventPage from './EventPage'

export const eventRoute = createRoute({
  path: 'events/$eventId',
  getParentRoute: () => rootRoute,
  component: (): ReactElement => (<Outlet />),

  notFoundComponent: () => <p>This setting page doesn&apos;t exist!</p>,
})

export const eventIndexRoute = createRoute({
  path: '/',
  getParentRoute: () => eventRoute,
  component: EventPage
})
