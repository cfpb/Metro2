import type { ReactElement } from 'react'
import { getRouteApi } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Summary from './AccountSummary'
import account from '../../fixtures/account.json'

export default function AccountPage(): ReactElement {
	const routeApi = getRouteApi('/events/$eventId/accounts/$accountId')
  const { eventId } = routeApi.useParams()

	return (
		<>
			<LocatorBar eyebrow='Account'
							    heading={ account.cons_acct_num }
                  breadcrumbs/>
			<Summary accountData={ account } eventId={eventId}/>
		</>
	)
}
