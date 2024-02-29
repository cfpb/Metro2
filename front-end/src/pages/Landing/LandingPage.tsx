import type { ReactElement } from 'react'
import LocatorBar from 'components/LocatorBar/LocatorBar'

export default function LandingPage(): ReactElement {
	return (
    <LocatorBar eyebrow='Welcome, Test User'
                heading='Here is your events list'/>    
	)
}
