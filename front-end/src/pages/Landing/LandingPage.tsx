import type { ReactElement } from 'react'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import EventList from './EventList'
import userData from '../../fixtures/user.json'

export default function LandingPage(): ReactElement {
	return (
    <>
      <LocatorBar eyebrow={ `Welcome, ${ userData.username }` }
                  heading='Here is your events list'/>
      <EventList events={ userData.assigned_events }
                 heading='Active'/>
    </>
	)
}
