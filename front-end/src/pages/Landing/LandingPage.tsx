import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import type User from '@src/types/User'
import { useLoaderData } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import EventList from './components/EventList/EventList'

export default function LandingPage(): ReactElement {
  const userData: User = useLoaderData({ from: '/' })
  // const { data: userData } = useUserData()

  return (
    <>
      <LocatorBar
        eyebrow={`Welcome, ${userData.username}`}
        heading='Here are your assigned events'
        icon='bank-round'
      />

      {userData.assigned_events.length > 0 ? (
        <EventList events={userData.assigned_events} />
      ) : null}
    </>
  )
}
