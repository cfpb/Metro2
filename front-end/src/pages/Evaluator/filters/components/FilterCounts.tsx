import { Button } from '@cfpb/design-system-react'
import Loader from '@src/components/Loader/Loader'
import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import { useEvaluatorFacets } from '@src/queries/evaluatorFacets'
import { useQueryClient } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { useState, type ReactElement } from 'react'
import Filters from './Filters'
interface FilterCountsData {
  evaluatorId: string
  eventId: string | number
}

export default function FilterCounts({
  evaluatorId,
  eventId
}: FilterCountsData): ReactElement {
  // Tracks whether user has cancelled fetching the counts data.
  const [isCancelled, setIsCancelled] = useState(false)

  const queryClient = useQueryClient()
  const key = ['event', String(eventId), 'evaluator', evaluatorId, 'facets', '']

  // Get the query params for current evaluator view
  const query: EvaluatorSearch = useSearch({ strict: false })

  // Fetch unfiltered counts to determine which filters / groups should be shown as inactive.
  const {
    data: allFacets,
    isFetching: isFetchingAllFacets,
    isError: isAllFacetsError
  } = useEvaluatorFacets(eventId, evaluatorId)

  // Fetch filtered counts for display.
  const {
    data: filteredFacets,
    isFetching: isFetchingFilteredFacets,
    isError: isFilteredFacetsError
  } = useEvaluatorFacets(eventId, evaluatorId, query)

  // Allow user to cancel counts requests if they are taking too long.
  const stopFetchingCounts = (event: React.MouseEvent<HTMLButtonElement>): void => {
    event.preventDefault()
    void queryClient.cancelQueries({ queryKey: key })
    setIsCancelled(true)
  }

  // show loader while fetching data
  if (isFetchingFilteredFacets || isFetchingAllFacets) {
    return (
      <div className='loader__wrapper'>
        <Loader message='' hasBackground={false} isOverlay={false}>
          <div data-testId='filter-loader'>
            <p>
              <b>Loading filter counts.</b>
              <br />
              This may take up to 30 seconds.
            </p>
            <p>
              If this is taking too long, you can use the filters without counts.
            </p>
            <Button data-testId='cancel-counts' onClick={stopFetchingCounts}>
              Show filters without counts
            </Button>
          </div>
        </Loader>
      </div>
    )
  }

  // Show message & filters without counts if there's an error fetching data.
  if (isAllFacetsError || isFilteredFacetsError) {
    return (
      <Filters message='Filter counts are not currently available. Try refreshing the page or contact an admin if the problem persists.' />
    )
  }

  // Show filters without counts if user cancels data request.
  if (isCancelled) {
    return <Filters />
  }

  // Show filters with counts if data is returned successfully.
  return (
    <Filters
      counts={allFacets?.facets}
      filteredCounts={filteredFacets?.facets}
      showCounts={true}
    />
  )
}
