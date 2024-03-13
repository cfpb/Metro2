import type { ReactElement } from 'react';
import { createRoute, Outlet, createFileRoute } from '@tanstack/react-router'
import rootRoute from '../rootRoute'
import EventPage from './EventPage'

export const eventRoute = createRoute({
  path: 'events/$eventId',
  getParentRoute: () => rootRoute,
  component: (): ReactElement => (<Outlet />),

  notFoundComponent: () => {
    return <p>This setting page doesn't exist!</p>
  },
})

export const eventIndexRoute = createRoute({
  path: '/',
  getParentRoute: () => eventRoute,
  component: EventPage
})

export const Route = createFileRoute('/events/$eventId')({
  component: () => {
    return (
      <div>
        <p>Settings page</p>
        <Outlet />
      </div>
    )
  },
  notFoundComponent: () => {
    return <p>This setting page doesn't exist!</p>
  },
})