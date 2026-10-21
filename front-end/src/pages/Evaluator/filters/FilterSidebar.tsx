import Loader from '@src/components/Loader/Loader'
import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import { useEvaluatorFacets } from '@src/queries/evaluatorFacets'
import { useSearch } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import Filters from './components/Filters'
import './FilterSidebar.scss'

interface EvaluatorSidebarData {
  evaluatorId: string
  eventId: string | number
}

export default function EvaluatorFilterSidebar({
  evaluatorId,
  eventId
}: EvaluatorSidebarData): ReactElement {
  const query: EvaluatorSearch = useSearch({ strict: false })

  // Fetch all filter counts data from server
  const { data: allFacets, isFetching: isFetchingAllFacets } = useEvaluatorFacets(
    eventId,
    evaluatorId
  )

  // Fetch filter counts data for currently applied filters from server
  const { data: filteredFacets, isFetching: isFetchingFilteredFacets } =
    useEvaluatorFacets(eventId, evaluatorId, query)

  const counts = allFacets?.facets
  const filteredCounts = filteredFacets?.facets

  return (
    <div className='loader__wrapper'>
      {isFetchingFilteredFacets || isFetchingAllFacets ? (
        <Loader message='Loading filter counts' className='lighter' />
      ) : (
        <Filters counts={counts} filteredCounts={filteredCounts} showCounts={true} />
      )}
    </div>
  )
}
