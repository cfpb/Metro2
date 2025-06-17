import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type { ReactElement } from 'react'
import type User from 'types/User'
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
