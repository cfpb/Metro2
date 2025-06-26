import type { UseQueryOptions, UseQueryResult } from '@tanstack/react-query'
import { keepPreviousData, queryOptions, useQuery } from '@tanstack/react-query'
import type EvaluatorHits from 'types/EvaluatorHits'
import { annotateAccountRecords } from 'utils/annotations'
import { stringifySearchParams } from 'utils/customStringify'
import fetchData from 'utils/fetchData'

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
  query: object = {},
  additionalParams: object = {}
): UseQueryOptions<EvaluatorHits, Error, EvaluatorHits, string[]> => {
  // Strip boolean filter 'any' values from query
  // since this is functionally equivalent to applying no filter
  const queryCopy = { ...query }
  for (const field of ['dofd', 'date_closed']) {
    if (queryCopy[field as keyof typeof queryCopy] === 'any') {
      // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
      delete queryCopy[field as keyof typeof queryCopy]
    }
  }
  const searchParams = stringifySearchParams(queryCopy)
  const key = ['event', eventId, 'evaluator', evaluatorId, 'query', searchParams]
  return queryOptions({
    queryKey: key,
    queryFn: async () => fetchEvaluatorHits(eventId, evaluatorId, searchParams),
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData,
    ...additionalParams
  })
}

export const useEvaluatorResults = (
  eventId: number | string,
  evaluatorId: number | string,
  query: object,
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
