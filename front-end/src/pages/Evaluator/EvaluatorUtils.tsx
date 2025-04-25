import type EvaluatorMetadata from 'types/Evaluator'
import { M2_FIELD_NAMES } from 'utils/constants'
import { formatNumber } from 'utils/formatters'

export const ITEMS_PER_PAGE = 200

/**
 * getPageCount()
 *
 * Divides results count by number of items displayed per page
 * to get number of pages in the current set of evaluator results.
 *
 * @param {number} resultsCount - the total number of results
 * @returns {number} The number of pages in the results
 * @example resultsCount: 2100
 *          returns: 11
 */

export const getPageCount = (resultsCount: number): number =>
  resultsCount === 0 ? 0 : Math.ceil(resultsCount / ITEMS_PER_PAGE)

/**
 * getResultsMessage()
 *
 * Returns a results message for 4 different scenarios:
 *     1. Sample view when there are more than 20 total hits:
 *           Showing representative sample of 20 out of {total} results
 *     2. Sample view when there are fewer than 20 total hits:
 *           Showing {total} out of {total} results
 *     3. All results view with no filters:
 *           Showing {total} results
 *     4. All results view with filters applied:
 *           Showing {x} matches out of {total} results
 *
 * @param {number} currentHitsCount - hits count for current request to evaluator
 *                                    results endpoint
 * @param {number} totalResultsCount - total hits on evaluator for this event
 * @param {number} rowsCount - number of rows returned from evaluator results endpoint
 * @param {string} view - whether sample or all results are being displayed
 * @param {boolean} isFiltered - whether data filters were included
 *                               in this request to evaluator results endpoint
 * @returns {string} - a results count message
 */

export const getResultsMessage = (
  currentHitsCount: number,
  totalResultsCount: number,
  rowsCount: number,
  view: 'all' | 'sample' | undefined = 'sample',
  isFiltered?: boolean
): string => {
  if (view === 'sample')
    return `Showing ${
      totalResultsCount > 20 ? 'representative sample of' : ''
    } ${rowsCount} out of ${formatNumber(totalResultsCount)} results`

  return isFiltered
    ? `Showing ${formatNumber(currentHitsCount)} matches out of ${formatNumber(
        totalResultsCount
      )} total results`
    : `Showing ${formatNumber(totalResultsCount)} results`
}

export const explanatoryFields = new Map([
  ['rationale', 'Rationale'],
  ['potential_harm', 'Potential harm'],
  ['crrg_reference', 'CRRG reference'],
  ['alternate_explanation', 'Alternate explanation']
])

/**
 * sortExplanatoryFields()
 *
 * An evaluator's metadata contains four fields that are displayed
 * in the 'How to evaluate these results' section of the evaluator page.
 * Most of the fields won't have content at first, so we separate the
 * fields into two arrays based on whether they're populated and display
 * the lists separately.
 *
 * @param {array} metadata - an object containing metadata about an evaluator
 * @returns {array} Returns an array containing two lists:
 *                    1. the explanatory fields that have values in the metadata
 *                    2. the explanatory fields that don't have values in the metadata
 * @example metadata = {rationale: '', potential_harm: 'Lorem ipsum', alternate_explanation: 'Lorem ipsum'}
 *          returns: [
 *                    ['potential_harm', 'alternate_explanation'],
 *                    ['rationale', 'crrg_reference']
 *                   ]
 */

export const sortExplanatoryFields = (
  metadata: EvaluatorMetadata
): [string[], string[]] => {
  const populatedFields: string[] = []
  const emptyFields: string[] = []
  for (const [field] of explanatoryFields.entries()) {
    if (metadata[field as keyof EvaluatorMetadata]) {
      populatedFields.push(field)
    } else {
      emptyFields.push(field)
    }
  }
  return [populatedFields, emptyFields]
}

/**
 * getTableFields()
 *
 * Generate list of fields that will appear as columns in the table for this evaluator's
 * results.
 *
 * The results table for each evaluator shows a custom subset of M2 fields that are useful
 * for understanding the scenario the specific evaluator is targeting.
 *
 * The list of fields displayed in the table is created by combining two lists from the evaluator's metadata
 * (fields_used--fields that are actually checked by the evaluator, & fields_display--other helpful fields)
 * with some default fields that are shown for each evaluator.
 *
 * Then we sort the list of fields by the order of the keys in M2_FIELD_NAMES to match
 * the order of the fields in the M2 data, and add a field for the first character of PHP
 * (one of the default fields) directly after the index of PHP.
 * (We use the first character of the 24 character payment history profile field in evaluators,
 * but php1 values are separated out on the front end and not returned from the API.)
 *
 * @param {array} fields_used - list of fields used by this eval
 * @param {array} fields_display - list of fields that are also relevant to this eval
 * @returns {array} Returns a list of fields that will be columns in the results table
 */

const defaultFields = [
  // 'id',
  'cons_acct_num',
  'activity_date',
  'doai',
  'acct_stat',
  'compl_cond_cd',
  'php',
  'pmt_rating',
  'spc_com_cd',
  'terms_freq',
  'dofd',
  'date_closed',
  'amt_past_due',
  'current_bal',
  'account_holder__cons_info_ind',
  'account_holder__cons_info_ind_assoc',
  'l1__change_ind'
]

export const getTableFields = (
  fields_used: string[],
  fields_display: string[]
): string[] => {
  const order = [...M2_FIELD_NAMES.keys()]
  const tableFields = [
    ...new Set([...fields_used, ...fields_display, ...defaultFields])
  ]
  const sortedFields = tableFields.sort((a, b) =>
    order.indexOf(a) > order.indexOf(b) ? 1 : -1
  )
  sortedFields.splice(sortedFields.indexOf('php') + 1, 0, 'php1')
  return sortedFields
}
