import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type Account from 'types/Account'
import type Event from 'types/Event'
import AccountDownloader from './components/Downloader'
import AccountOverview from './components/Overview'
import { getColDefs } from './utils/getColDefs'
import getTableFields from './utils/getTableFields'

export default function AccountPage(): ReactElement {
  // Get event and account data from loaders
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const accountData: Account = useLoaderData({
    from: '/events/$eventId/accounts/$accountId'
  })

  // Generate list of fields and column definitions for the account records table
  const fields = getTableFields()
  const colDefs = getColDefs(fields, accountData.inconsistencies)

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
            href: `/events/${String(eventData.id)}`,
            text: 'Back to event results'
          }
        ]}
      />
      <div className='row row__content row__summary'>
        <AccountOverview accountData={accountData} eventData={eventData} />
      </div>
      <div className='row row__download u-mt0 u-mb0'>
        <AccountDownloader
          rows={rows}
          fields={fields}
          accountId={accountData.cons_acct_num}
          eventData={eventData}
        />
      </div>
      <div className='row row__content'>
        <Table rows={rows} columnDefinitions={colDefs} />
      </div>
    </>
  )
}
