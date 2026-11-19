import type { EvaluatorSearch } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'
import type { EvaluatorFacetData } from '@src/types/EvaluatorFacets'
import { stringifySearchParams } from '@src/utils/customStringify'
// import fetchData from '@src/utils/fetchData'
import type { UseQueryOptions, UseQueryResult } from '@tanstack/react-query'
import { keepPreviousData, queryOptions, useQuery } from '@tanstack/react-query'

export const fetchEvaluatorFacets = async (
  eventId: string,
  evaluatorId: string,
  searchParameters: string,
  signal: AbortSignal
): Promise<EvaluatorFacetData> => {
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/facets/${searchParameters}`
  try {
    // await new Promise(r => setTimeout(r, 77_777))
    const response = await fetch(url, { signal })
    if (response.ok) return (await response.json()) as EvaluatorFacetData
    throw new Error(String(response.status))
  } catch (error) {
    throw new Error('Facets error', { cause: error })
  }
}

export const evaluatorFacetsQueryOptions = (
  eventId: string,
  evaluatorId: string,
  query: EvaluatorSearch | Record<PropertyKey, never> = {}
): UseQueryOptions<EvaluatorFacetData, Error, EvaluatorFacetData, string[]> => {
  // get a list of filters in the querystring that affect facet counts
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { page, page_size, view, sort, ...filters } = query
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
    queryFn: async ({ signal }) =>
      fetchEvaluatorFacets(eventId, evaluatorId, searchParameters, signal),
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData,
    retry: 1
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
