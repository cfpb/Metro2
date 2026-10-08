import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import AccountRecord from '@src/types/AccountRecord'
import type EvaluatorHits from '@src/types/EvaluatorHits'
import { annotateAccountRecords } from '@src/utils/annotations'
import { stringifySearchParams } from '@src/utils/customStringify'
import fetchData from '@src/utils/fetchData'
import type { UseQueryOptions, UseQueryResult } from '@tanstack/react-query'
import { keepPreviousData, queryOptions, useQuery } from '@tanstack/react-query'

export const fetchHitsForDownload = async (
  eventId: string,
  evaluatorId: string,
  query: EvaluatorSearch
): Promise<AccountRecord[]> => {
  const searchParams = stringifySearchParams(query)
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/${searchParams}`
  try {
    const response = await fetch(url)
    if (response.ok) {
      const data = (await response.json()) as EvaluatorHits
      return annotateAccountRecords(data.hits)
    }
    throw new Error(String(response.status))
  } catch (error) {
    throw new Error('Hits download error', { cause: error })
  }
}

export const fetchEvaluatorHits = async (
  eventId: string,
  evaluatorId: string,
  searchParams: string
): Promise<EvaluatorHits> => {
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/${searchParams}`
  const data: EvaluatorHits = await fetchData(url, 'hits')
  return { count: data.count, hits: annotateAccountRecords(data.hits) }
}

export const evaluatorHitsQueryOptions = (
  eventId: string,
  evaluatorId: string,
  query: EvaluatorSearch,
  additionalParams: object = {}
): UseQueryOptions<EvaluatorHits, Error, EvaluatorHits, string[]> => {
  let queryObj
  if (query.view === 'all') {
    // In the all results view, we need to update the results data
    // any time a query param changes, so we copy the full query to use as part
    // of the queryKey.
    // If the 'dofd' or 'date_closed' filter value is set to 'any', though, we
    // strip that param since it's functionally equivalent to applying no filter.
    queryObj = { ...query }
    for (const field of ['dofd', 'date_closed']) {
      if (queryObj[field] === 'any') delete queryObj[field]
    }
  } else {
    // Filters aren't available on the sample view and we don't want to refetch
    // data when sort values are applied, so we only need to use the view param
    // in the queryKey.
    queryObj = { view: 'sample' }
  }
  const searchParams = stringifySearchParams(queryObj)
  const key = ['event', eventId, 'evaluator', evaluatorId, 'query', searchParams]
  return queryOptions({
    queryKey: key,
    queryFn: async () => fetchEvaluatorHits(eventId, evaluatorId, searchParams),
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData,
    retry: (failureCount, error) => {
      // Don't retry if 404 -- that probably indicates an invalid page
      return !(error.message === '404' || failureCount > 3);
    },
    ...additionalParams
  })
}

export const useEvaluatorResults = (
  eventId: number | string,
  evaluatorId: number | string,
  query: EvaluatorSearch,
  additionalParams?: object
): UseQueryResult<EvaluatorHits> =>
  useQuery<EvaluatorHits, Error, EvaluatorHits, string[]>(
    evaluatorHitsQueryOptions(
      String(eventId),
      String(evaluatorId),
      query,
      additionalParams
    )
  )
