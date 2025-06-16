import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import type AccountHolder from 'types/AccountHolder'
import fetchData from 'utils/fetchData'

export const fetchAccountHolderData = async (
  eventId: number,
  accountId: string
): Promise<AccountHolder> => {
  const url = `/api/events/${eventId}/account/${accountId}/account_holder/`
  return fetchData<AccountHolder>(url, 'account')
}

export const accountHolderQueryOptions = (
  eventId: number,
  accountId: string
): UseQueryOptions<AccountHolder, Error, AccountHolder, (number | string)[]> =>
  queryOptions({
    queryKey: ['event', eventId, 'accountHolder', accountId],
    queryFn: async (): Promise<AccountHolder> =>
      fetchAccountHolderData(eventId, accountId),
    enabled: false,
    staleTime: Number.POSITIVE_INFINITY
  })
