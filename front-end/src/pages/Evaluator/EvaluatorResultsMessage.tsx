import type { ReactElement } from 'react'
import { formatNumber } from 'utils/formatters'
import { ITEMS_PER_PAGE } from './EvaluatorUtils'

/**
 * EvaluatorResultsMessage
 *
 * Returns a results message for 4 different scenarios:
 *     1. Sample view when there are more than 20 total hits:
 *           Showing 20 sample results
 *     2. All results view with no filters OR sample view with < 20 total hits:
 *           Showing {x} - {y} of {total} results
 *     3. All results view with filters applied & results:
 *           Showing {x} - {y} of {total} filtered results
 *     4. All results view with filters and no results:
 *           Showing 0 results
 *
 * @param {number} currentHitsCount - hits count for current request to evaluator
 *                                    results endpoint
 * @param {number} totalResultsCount - total hits on evaluator for this event
 * @param {number} page - current page
 * @param {number} pageSize - how many items to view per page
 * @param {string} view - whether sample or all results are being displayed
 * @param {boolean} isFiltered - whether data filters were included
 *                               in this request to evaluator results endpoint
 * @returns {string} - a results count message
 */

interface EvaluatorResultsMessageProps {
  currentHitsCount: number
  totalResultsCount: number
  page?: number
  pageSize?: number
  view?: 'all' | 'sample'
  isFiltered: boolean
}

export default function EvaluatorResultsMessage({
  currentHitsCount,
  totalResultsCount,
  page = 1,
  pageSize = ITEMS_PER_PAGE,
  view = 'sample',
  isFiltered
}: EvaluatorResultsMessageProps): ReactElement {
  let message = ''

  if (view === 'sample' && totalResultsCount > 20) {
    message = 'Showing 20 sample results'
  } else if (isFiltered && currentHitsCount === 0) {
    message = 'Showing 0 results'
  } else {
    const start = (page - 1) * pageSize + 1
    const end =
      page * pageSize > currentHitsCount ? currentHitsCount : page * pageSize
    message = `Showing ${formatNumber(start)} - ${formatNumber(
      end
    )} of ${formatNumber(currentHitsCount)} ${isFiltered ? 'filtered' : ''} results`
  }

  return <h4>{message}</h4>
}
