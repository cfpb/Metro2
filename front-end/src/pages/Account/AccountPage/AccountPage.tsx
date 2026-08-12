import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import Table from '@src/components/Table/Table'
import { useAccountSuspense } from '@src/queries/account'
import { useEventSuspense } from '@src/queries/event'
import { getRouteApi } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import AccountDownloader from './components/Downloader'
import AccountOverview from './components/Overview'
import { accountTableFields } from './utils/accountTableFields'
import { getColDefs } from './utils/getColDefs'

export default function AccountPage(): ReactElement {
  const { eventId, accountId } = getRouteApi(
    '/events/$eventId/accounts/$accountId'
  ).useParams()
  const eventData = useEventSuspense(eventId)
  const accountData = useAccountSuspense(eventId, accountId)

  // Generate list of fields and column definitions for the account records table
  const colDefs = getColDefs(accountTableFields, accountData.inconsistencies)

  // Get all records for this account to show in the table
  const rows = accountData.account_activity

  return (
    <>
      <LocatorBar
        eyebrow='Account'
        heading={accountData.cons_acct_num}
        icon='user-round'
        breadcrumbs={[
          {
            to: `/events/${String(eventData.id)}`,
            label: 'Back to event results'
          }
        ]}
      />
      <div className='row row--content row--summary'>
        <AccountOverview accountData={accountData} eventData={eventData} />
      </div>
      <div className='row row--right u-mt0 u-mb0'>
        <AccountDownloader
          rows={rows}
          fields={accountTableFields}
          accountId={accountData.cons_acct_num}
          eventData={eventData}
        />
      </div>
      <div className='row row--content'>
        <Table
          rows={rows}
          columnDefinitions={colDefs}
          defaultSort={['activity_date']}
        />
      </div>
    </>
  )
}
