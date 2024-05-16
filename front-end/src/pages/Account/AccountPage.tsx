import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { M2_FIELDS } from 'utils/constants'
import { annotateData, generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import AccountDownloader from './AccountDownloader'
import Summary from './AccountSummary'

const colDefs = generateColumnDefinitions(M2_FIELDS, ['activity_date'])

export default function AccountPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const accountData: Account = useLoaderData({
    from: '/events/$eventId/accounts/$accountId'
  })
  const rows = annotateData(accountData.account_activity)

  return (
    <>
      <LocatorBar
        eyebrow='Account'
        heading={accountData.cons_acct_num}
        icon='user-round'
        breadcrumbs
      />
      <Summary accountData={accountData} eventId={eventData.name} />

      <div className='content-row'>
        <div className='download-row'>
          <AccountDownloader
            rows={rows}
            fields={M2_FIELDS}
            accountId={accountData.cons_acct_num}
            eventData={eventData}
          />
        </div>
        <Table rows={rows} columnDefinitions={colDefs} />
      </div>
    </>
  )
}
