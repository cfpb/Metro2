import { useLoaderData } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { M2_FIELDS } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import AccountDownloader from './AccountDownloader'
import Summary from './AccountSummary'

// Generate a column definition for the inconsistencies column
// Pass the inconsistencies legend for this account in cellRendererParams
// In cellRenderer, replace evaluator ids in the record's inconsistencies list
// with their index in the legend
const getInconsistenciesColDef = (accountInconsistencies: string[]): ColDef => ({
  field: 'inconsistencies',
  headerName: 'Inconsistencies',
  cellRendererParams: { accountInconsistencies },
  cellDataType: false,
  cellRenderer: ({ value }: { value: [] }): ReactElement => (
    <> {value.map(item => accountInconsistencies.indexOf(item) + 1).join(', ')}</>
  )
})

export default function AccountPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const accountData: Account = useLoaderData({
    from: '/events/$eventId/accounts/$accountId'
  })
  const rows = accountData.account_activity
  const colDefs = generateColumnDefinitions(M2_FIELDS, ['activity_date'])

  // Add inconsistencies column definition
  const inconsistenciesColDef = getInconsistenciesColDef(accountData.inconsistencies)
  colDefs.splice(1, 0, inconsistenciesColDef)

  // Add inconsistencies to fields
  const fields = [...M2_FIELDS]
  fields.splice(1, 0, 'inconsistencies')

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
