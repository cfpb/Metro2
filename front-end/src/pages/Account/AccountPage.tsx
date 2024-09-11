import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import { COL_DEF_CONSTANTS, M2_FIELD_NAMES } from 'utils/constants'
import { generateColumnDefinitions } from 'utils/utils'
import type Account from './Account'
import AccountDownloader from './AccountDownloader'
import Summary from './AccountSummary'

// Generate a column definition for the inconsistencies column
// Pass the inconsistencies legend for this account in cellRendererParams
// In cellRenderer, replace evaluator ids in the record's inconsistencies list
// with their index in the legend
const getInconsistenciesColDef = (accountInconsistencies: string[]): object => ({
  cellRendererParams: { accountInconsistencies },
  cellDataType: false,
  cellRenderer: ({ value }: { value: [] }): ReactElement => (
    <>{value.map(item => accountInconsistencies.indexOf(item) + 1).join(', ')}</>
  ),
  minWidth: 175
})

// TODO: should we be getting / showing cons_acct_num for L1 evals?
// TODO: should we be showing the name values for PROG-DOFD-3?
// Get fields from M2_FIELD_NAMES
// remove cons_acct_num since we're not currently getting it from API
// remove account holder name values unless the account hit on PROG-DOFD-3, which uses them
// and add 'inconsistencies' at position 2
const getFields = (inconsistencies: string[]): string[] => {
  const fields = [...M2_FIELD_NAMES.keys()].filter(field => {
    let screen = ['cons_acct_num']
    if (!inconsistencies.includes('PROG-DOFD-3')) {
      screen = [
        ...screen,
        'previous_values__account_holder__first_name',
        'previous_values__account_holder__surname',
        'account_holder__first_name',
        'account_holder__surname'
      ]
    }
    return !screen.includes(field)
  })
  fields.splice(1, 0, 'inconsistencies')
  return fields
}

export default function AccountPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const accountData: Account = useLoaderData({
    from: '/events/$eventId/accounts/$accountId'
  })
  const fields = getFields(accountData.inconsistencies)
  const rows = accountData.account_activity

  // TODO: Move this all into a col def generation helper function
  const colDefProps = {
    ...COL_DEF_CONSTANTS,
    inconsistencies: getInconsistenciesColDef(accountData.inconsistencies),
    activity_date: { pinned: 'left', type: 'formattedDate', minWidth: 160 }
  }
  const colDefs = generateColumnDefinitions(fields, colDefProps)
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
      <Summary accountData={accountData} eventData={eventData} />

      <div className='content-row'>
        <div className='download-row'>
          <AccountDownloader
            rows={rows}
            fields={fields}
            accountId={accountData.cons_acct_num}
            eventData={eventData}
          />
        </div>
        <Table rows={rows} columnDefinitions={colDefs} />
      </div>
    </>
  )
}
