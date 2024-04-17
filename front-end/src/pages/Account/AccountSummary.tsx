import { Link } from '@tanstack/react-router'
import type { Definition } from 'components/DefinitionList/DefinitionList'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import type { ReactElement } from 'react'
import type { AccountRecord } from '../../utils/constants'
import { FIELD_NAMES_LOOKUP } from '../../utils/constants'
import { getM2Definition } from '../../utils/utils'
import type Account from './Account'
import AccountHolderComponent from './AccountHolderComponent'

interface AccountSummaryProperties {
  accountData: Account
  eventId: string
}

const summaryFields = [
  'port_type',
  'acct_type',
  'terms_dur',
  'terms_freq',
  'date_open'
] as const

// Given an account activity record, returns an array of Definition objects
// for summary fields with format:
// {
//   definition: field name from FIELD_NAMES_LOOKUP
//   term: field's value from record plus annotation if available
// }
// Adds an additional object to conditionally display account holder's PII
// with format:
// {
//  definition: Contact Information,
//  term: React component that fetches or displays contact information
// }
export const getSummaryItems = (
  record: AccountRecord,
  contactComponent: ReactElement
): Definition[] => {
  const summaryItems: Definition[] = summaryFields.map(field => {
    const value = record[field]
    const definition = getM2Definition(field, value)
    return {
      term: FIELD_NAMES_LOOKUP[field],
      definition: definition ?? value
    }
  })
  summaryItems.unshift({
    term: 'Contact Information',
    definition: contactComponent
  })
  return summaryItems
}

export default function AccountSummary({
  accountData,
  eventId
}: AccountSummaryProperties): ReactElement {
  // Get latest activity record for account
  // TODO: ensure records are sorted by date or sort them
  const latestRecord = accountData.account_activity[0]
  const contactComponent = (
    <AccountHolderComponent
      eventId={eventId}
      accountId={accountData.cons_acct_num}
    />
  )

  return (
    <div className='content-row u-mt15'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3' data-testid='details'>
          <h3>Account Details</h3>
          <DefinitionList items={getSummaryItems(latestRecord, contactComponent)} />
        </div>
        {accountData.inconsistencies.length > 0 ? (
          <div
            className='content-l_col content-l_col-1-3'
            data-testid='inconsistencies'>
            <h3>Inconsistencies found</h3>
            <ul>
              {accountData.inconsistencies.map(inconsistency => (
                <li key={inconsistency.id}>
                  <Link
                    to='/events/$eventId/evaluators/$evaluatorId'
                    params={{ eventId, evaluatorId: inconsistency.id }}>
                    {inconsistency.name || inconsistency.id}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </div>
  )
}
