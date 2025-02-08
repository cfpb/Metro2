import type { UseQueryOptions } from '@tanstack/react-query'
import { keepPreviousData, queryOptions } from '@tanstack/react-query'

import type { AccountRecord } from 'utils/constants'
import {
  fetchData,
  prepareAccountRecordData,
  stringifySearchParams
} from 'utils/utils'

export interface EvaluatorHits {
  hits: AccountRecord[]
}

export const fetchEvaluatorHits = async (
  eventId: string,
  evaluatorId: string,
  searchParams: string
): Promise<AccountRecord[]> => {
  const url = `/api/events/${eventId}/evaluator/${evaluatorId}/${searchParams}`
  const data: EvaluatorHits = await fetchData(url, 'hits', 500)
  return prepareAccountRecordData(data.hits)
}

export const evaluatorHitsQueryOptions = (
  eventId: string,
  evaluatorId: string,
  query: object = {}
): UseQueryOptions<AccountRecord[], Error, AccountRecord[], string[]> => {
  const searchParams = stringifySearchParams(query)
  const key = ['event', eventId, 'evaluator', evaluatorId, 'query', searchParams]
  return queryOptions({
    queryKey: key,
    queryFn: async () => fetchEvaluatorHits(eventId, evaluatorId, searchParams),
    staleTime: 60 * 1000,
    placeholderData: keepPreviousData
  })
}
