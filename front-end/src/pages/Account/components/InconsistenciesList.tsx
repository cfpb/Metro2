import type Event from '@src/types/Event'
import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'

import { ITEMS_PER_PAGE } from '@src/constants/settings'
import getEvaluatorDataFromEvent from 'utils/getEvaluatorFromEvent'

interface InconsistenciesListProperties {
  inconsistencies: string[]
  eventData: Event
}

/**
 * AccountInconsistenciesList()
 *
 * Takes an array of names of evaluators with hits on any of this
 * account's records.
 *
 * Returns a numbered list containing links for each of these evaluators.
 * The link text includes the evaluator's name and its short description and
 * the link goes to this event's page for the evaluator.
 *
 * The list serves as a legend for the account records table -- each row
 * in the table shows numbers corresponding to this list for any inconsistencies
 * flagged on the row's account record.
 *
 * @param {object} latestAccountRecord - most recent record for this account
 * @param {number} eventId - the id of the current event
 * @returns {ReactElement}
 */

export default function AccountInconsistenciesList({
  inconsistencies,
  eventData
}: InconsistenciesListProperties): ReactElement {
  return (
    <ol>
      {inconsistencies.map(inconsistency => (
        <li key={inconsistency}>
          <Link
            to='/events/$eventId/evaluators/$evaluatorId'
            params={{
              eventId: String(eventData.id),
              evaluatorId: inconsistency
            }}
            search={{
              page: 1,
              view: 'sample',
              page_size: ITEMS_PER_PAGE
            }}>
            {inconsistency}
          </Link>
          <span>
            {' '}
            {getEvaluatorDataFromEvent(eventData, inconsistency)?.description}
          </span>
        </li>
      ))}
    </ol>
  )
}
