import type { Definition } from 'components/DefinitionList/DefinitionList'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import type { ReactElement } from 'react'

import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import type AccountRecord from 'types/AccountRecord'
import { getM2Definition } from 'utils/annotations'
import { formatDate } from 'utils/formatDates'
import getHeaderName from 'utils/getHeaderName'
import AccountContactInformation from './ContactInformation'

interface AccountSummaryProperties {
  latestAccountRecord: AccountRecord
  eventId: number
}

const summaryFields = [
  'port_type',
  'acct_type',
  'terms_dur',
  'terms_freq',
  'date_open'
] as const

/**
 * AccountSummary()
 *
 * Using the latest activity record for an account, generates a
 * definition list containing the titles and values (plus annotation,
 * where available) for five key fields on the record.
 *
 * Also adds a "Contact information" entry to the list containing
 * a button that allows users to request and display contact info
 * for the account holder.
 *
 * @param {object} latestAccountRecord - most recent record for this account
 * @param {number} eventId - the id of the current event
 * @returns {ReactElement}
 */

export default function AccountSummary({
  latestAccountRecord,
  eventId
}: AccountSummaryProperties): ReactElement {
  const summaryItems: Definition[] = [
    {
      term: 'Contact Information',
      definition: (
        <AccountContactInformation
          accountId={String(latestAccountRecord.cons_acct_num)}
          eventId={eventId}
        />
      )
    }
  ]
  for (const field of summaryFields) {
    const value = latestAccountRecord[field]
    const definition =
      field === 'date_open' ? formatDate(value) : getM2Definition(field, value)
    summaryItems.push({
      term: getHeaderName(field, M2_FIELD_NAMES),
      definition: definition ?? value
    })
  }

  return <DefinitionList items={summaryItems} />
}
