import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type User from 'models/User'
import type { ReactElement } from 'react'
import EventList from './EventList'

export default function LandingPage(): ReactElement {
  const userData: User = useLoaderData({ from: '/' })

  return (
    <>
      <LocatorBar
        eyebrow={`Welcome, ${userData.username}`}
        heading='Here is your events list'
        icon='bank-round'
      />
      {userData.assigned_events.length > 0 ? (
        <EventList events={userData.assigned_events} />
      ) : null}
    </>
  )
}
