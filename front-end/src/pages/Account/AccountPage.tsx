import { getRouteApi } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import { M2_FIELDS } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import Summary from './AccountSummary'

const routeApi = getRouteApi('/events/$eventId/accounts/$accountId')

const colDefs = generateColumnDefinitions(M2_FIELDS, ['activity_date'])

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
      <Table rows={accountData.account_activity} columnDefinitions={colDefs} />
    </>
  )
}
