import { Hero } from '@cfpb/design-system-react'
import type User from '@src/types/User'
import { useLoaderData } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import EventList from './components/EventList/EventList'

export default function LandingPage(): ReactElement {
  const userData: User = useLoaderData({ from: '/' })
  // const { data: userData } = useUserData()

  return (
    <>
      <Hero
        backgroundColor='#eff8fd'
        heading='Find credit reporting inconsistencies with the Metro 2 Evaluator tool'
        subheading='Run error and consistency checks to find inaccuracies in Metro 2 credit reporting data, and share or download results for further analysis.'
        data-testid='landing-page-hero'
      />

      {userData.assigned_events.length > 0 ? (
        <EventList events={userData.assigned_events} />
      ) : null}
    </>
  )
}
