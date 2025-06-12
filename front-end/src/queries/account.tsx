import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import type Account from 'types/Account'
import { annotateAccountRecords } from 'utils/annotations'
import fetchData from 'utils/fetchData'

export const fetchAccount = async (
  eventId: string,
  accountId: string
): Promise<Account> => {
  const url = `/api/events/${eventId}/account/${accountId}/`
  const data = await fetchData<Account>(url, 'account')
  data.account_activity = annotateAccountRecords(data.account_activity)
  return data
}

export const accountQueryOptions = (
  eventId: string,
  accountId: string
): UseQueryOptions<Account, Error, unknown, string[]> =>
  queryOptions({
    queryKey: ['events', eventId, 'accounts', accountId],
    queryFn: async () => fetchAccount(eventId, accountId)
  })
