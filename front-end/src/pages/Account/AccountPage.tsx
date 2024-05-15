import { getRouteApi } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { M2_FIELDS } from 'utils/constants'
import { annotateData, generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import AccountDownloader from './AccountDownloader'
import Summary from './AccountSummary'

const routeApi = getRouteApi('/events/$eventId/accounts/$accountId')

const colDefs = generateColumnDefinitions(M2_FIELDS, ['activity_date'])

export const prepAccountData = (rows: AccountRecord[]): AccountRecord[] => {
  // Add a new php1 value to each row based on first character of php
  for (const row of rows) row.php1 = row.php?.charAt(0)
  // Add annotations where available to row values
  return annotateData(rows)
}

export default function AccountPage(): ReactElement {
  const { eventId }: { eventId: string } = routeApi.useParams()
  const accountData: Account = routeApi.useLoaderData()
  const rows = prepAccountData(accountData.account_activity)

  return (
    <>
      <LocatorBar
        eyebrow='Account'
        heading={accountData.cons_acct_num}
        icon='user-round'
        breadcrumbs
      />
      <Summary accountData={accountData} eventId={eventId} />

      <div className='content-row'>
        <div className='download-row'>
          <AccountDownloader rows={rows} fields={M2_FIELDS} />
        </div>
        <Table rows={rows} columnDefinitions={colDefs} />
      </div>
    </>
  )
}
