import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import type { EvaluatorFacetData } from '@src/types/EvaluatorFacets'
import { stringifySearchParams } from '@src/utils/customStringify'
import fetchData from '@src/utils/fetchData'
import type { UseQueryOptions, UseQueryResult } from '@tanstack/react-query'
import { keepPreviousData, queryOptions, useQuery } from '@tanstack/react-query'

export const fetchEvaluatorFacets = async (
  eventId: string,
  evaluatorId: string,
  searchParameters: string
): Promise<EvaluatorFacetData> => {
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/facets/${searchParameters}`
  return fetchData(url, 'facets')
}

export const evaluatorFacetsQueryOptions = (
  eventId: string,
  evaluatorId: string,
  query: EvaluatorSearch | Record<PropertyKey, never> = {}
): UseQueryOptions<EvaluatorFacetData, Error, EvaluatorFacetData, string[]> => {
  // get a list of filters in the querystring that affect facet counts
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { page, page_size, view, sort, show_counts, ...filters } = query
  // Stringify the list for use as a key to the counts cache
  const searchParameters = stringifySearchParams(filters)
  const key = [
    'event',
    eventId,
    'evaluator',
    evaluatorId,
    'facets',
    searchParameters
  ]
  return queryOptions({
    queryKey: key,
    queryFn: async () =>
      fetchEvaluatorFacets(eventId, evaluatorId, searchParameters),
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData,
    retry: (failureCount, error) => {
      // Don't retry if 404 -- that probably indicates an invalid page
      return !(error.message === '404' || failureCount > 3)
    }
  })
}

export const useEvaluatorFacets = (
  eventId: number | string,
  evaluatorId: number | string,
  query?: EvaluatorSearch
): UseQueryResult<EvaluatorFacetData> => {
  return useQuery<EvaluatorFacetData, Error, EvaluatorFacetData, string[]>(
    evaluatorFacetsQueryOptions(String(eventId), String(evaluatorId), query)
  )
}
