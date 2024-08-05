import { Link } from '@tanstack/react-router'
import type { Definition } from 'components/DefinitionList/DefinitionList'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import type Event from 'pages/Event/Event'
import type { ReactElement } from 'react'
import type { AccountRecord } from 'utils/constants'
import { M2_FIELD_NAMES } from 'utils/constants'
import {
  formatDate,
  getEvaluatorDataFromEvent,
  getHeaderName,
  getM2Definition
} from 'utils/utils'
import type Account from './Account'
import AccountContactInformation from './AccountContactInformation'

interface AccountSummaryProperties {
  accountData: Account
  eventData: Event
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
    const definition =
      field === 'date_open' ? formatDate(value) : getM2Definition(field, value)
    return {
      term: getHeaderName(field, M2_FIELD_NAMES),
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
  eventData
}: AccountSummaryProperties): ReactElement {
  // Get latest activity record for account
  // TODO: ensure records are sorted by date or sort them
  const latestRecord = accountData.account_activity[0]
  const contactComponent = (
    <AccountContactInformation
      eventId={eventData.id}
      accountId={accountData.cons_acct_num}
    />
  )

  return (
    <div className='content-row summary-row'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3' data-testid='details'>
          <h2>Account Details</h2>
          <DefinitionList items={getSummaryItems(latestRecord, contactComponent)} />
        </div>
        {accountData.inconsistencies.length > 0 ? (
          <div
            className='content-l_col content-l_col-1-3'
            data-testid='inconsistencies'>
            <h2>Inconsistencies found</h2>
            <ol>
              {accountData.inconsistencies.map(inconsistency => (
                <li key={inconsistency}>
                  <Link
                    to='/events/$eventId/evaluators/$evaluatorId'
                    params={{ eventId: eventData.id, evaluatorId: inconsistency }}>
                    {inconsistency}
                  </Link>
                  <span>
                    {' '}
                    {
                      getEvaluatorDataFromEvent(eventData, inconsistency)
                        ?.description
                    }
                  </span>
                </li>
              ))}
            </ol>
          </div>
        ) : null}
      </div>
    </div>
  )
}
