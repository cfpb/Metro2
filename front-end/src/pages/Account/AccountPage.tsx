import type { ReactElement } from 'react'
import LocatorBar from 'components/LocatorBar/LocatorBar'

export default function AccountPage(): ReactElement {
	return (
    <LocatorBar eyebrow='Account'
							  heading='999999999'
                breadcrumbs/>
	)
}
