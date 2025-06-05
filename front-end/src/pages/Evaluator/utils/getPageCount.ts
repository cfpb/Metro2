import ITEMS_PER_PAGE from './constants'

/**
 * getPageCount()
 *
 * Divides results count by number of items displayed per page
 * to get number of pages in the current set of evaluator results.
 *
 * @param {number} resultsCount - the total number of results
 * @param {number} page_size - the number of results to show per page
 * @returns {number} The number of pages in the results
 * @example resultsCount: 2100
 *          returns: 11
 */

const getPageCount = (
  resultsCount: number,
  page_size: number = ITEMS_PER_PAGE
): number => {
  if (page_size > resultsCount) return 1
  return resultsCount === 0 ? 0 : Math.ceil(resultsCount / page_size)
}

export default getPageCount
