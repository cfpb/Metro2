import type { ReactElement } from 'react'
import { Link } from '@tanstack/react-router'
import DefinitionList from 'components/DefinitionList/DefinitionList'
import { FIELD_NAMES_LOOKUP } from '../../utils/constants'
import getM2CodeDefinition from '../../utils/utils'
import type { Account } from './Account'

interface AccountSummaryProperties {
  accountData: Account,
  eventId: string
}

const summaryFields = [
  'port_type', 'acct_type', 'terms_dur', 'terms_freq', 'date_open'
] as const

export default function AccountSummary( {
  accountData,
  eventId
}: AccountSummaryProperties ): ReactElement {

  // Get latest activity record for account
  // TODO: ensure records are sorted by date or sort them
  const activityRecord = accountData.account_activity[0]

  // Pull data for summary fields from latest record &
  // look up human-readable definitions for coded values
  const summaryItems = summaryFields.map( field => {
    const value = activityRecord[field]
    const definition = getM2CodeDefinition(field, value)
    return {
      term: FIELD_NAMES_LOOKUP[field],
      definition: definition ?? value
    }
  })

	return (
    <div className='content-row u-mt15'>
      <div className='content-l'>
        <div className='content-l_col content-l_col-1-3'
             data-testid='details'>
          <h3>Account Details</h3>
          <DefinitionList items={ summaryItems }/>
        </div>
        { accountData.inconsistencies.length > 0
          ? <div className='content-l_col content-l_col-1-3'
                 data-testid='inconsistencies'>
              <h3>Inconsistencies found</h3>
              <ul>
              { accountData.inconsistencies.map( inconsistency => 
                <li key={ inconsistency.id }>
                  <Link to='/events/$eventId/evaluators/$evaluatorId'
                        params={{ eventId, evaluatorId: inconsistency.id}}>
                      { inconsistency.name }         
                  </Link>
                </li>     
              ) }
              </ul>
            </div>
        : null }
      </div>
    </div>
	)
}


