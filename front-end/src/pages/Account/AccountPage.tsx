import { getRouteApi } from '@tanstack/react-router'
import type { ColDef } from 'ag-grid-community'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import { M2_FIELDS } from 'utils/constants'
import { annotateData, generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import AccountDownloader from './AccountDownloader'
import Summary from './AccountSummary'

const routeApi = getRouteApi('/events/$eventId/accounts/$accountId')

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
  const { eventId }: { eventId: string } = routeApi.useParams()
  const accountData: Account = routeApi.useLoaderData()
  const rows = annotateData(accountData.account_activity)
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
      <Summary accountData={accountData} eventId={eventId} />

      <div className='content-row'>
        <div className='download-row'>
          <AccountDownloader rows={rows} fields={fields} />
        </div>
        <Table rows={rows} columnDefinitions={colDefs} />
      </div>
    </>
  )
}
