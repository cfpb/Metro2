import { getRouteApi } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import type { ReactElement } from 'react'
import type Account from './Account'
import Summary from './AccountSummary'

const routeApi = getRouteApi('/events/$eventId/accounts/$accountId')

export default function AccountPage(): ReactElement {
  const { eventId }: { eventId: string } = routeApi.useParams()
  const accountData: Account = routeApi.useLoaderData()

  return (
    <>
      <LocatorBar
        eyebrow='Account'
        heading={accountData.cons_acct_num}
        breadcrumbs
      />
      <Summary accountData={accountData} eventId={eventId} />
    </>
  )
}
