import type { ReactElement } from 'react'
import type Event from 'types/Event'

import type Account from 'types/Account'
import AccountInconsistenciesList from './InconsistenciesList'
import AccountSummary from './Summary'

interface AccountOverviewProperties {
  accountData: Account
  eventData: Event
}

export default function AccountOverview({
  accountData,
  eventData
}: AccountOverviewProperties): ReactElement {
  return (
    <div className='content-l'>
      <div className='content-l_col content-l_col-1-3' data-testid='details'>
        <h2>Account Details</h2>
        <AccountSummary
          latestAccountRecord={accountData.account_activity[0]}
          eventId={eventData.id}
        />
      </div>
      {accountData.inconsistencies.length > 0 ? (
        <div
          className='content-l_col content-l_col-1-3'
          data-testid='inconsistencies'>
          <h2>Inconsistencies found</h2>
          <AccountInconsistenciesList
            eventData={eventData}
            inconsistencies={accountData.inconsistencies}
          />
        </div>
      ) : null}
    </div>
  )
}
