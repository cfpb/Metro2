import type Account from '@src/types/Account'
import { annotateAccountRecords } from '@src/utils/annotations'
import fetchData from '@src/utils/fetchData'
import { queryOptions, useSuspenseQuery } from '@tanstack/react-query'

export const fetchAccount = async (
  eventId: string,
  accountId: string
): Promise<Account> => {
  const url = `/api/events/${eventId}/account/${accountId}/`
  const data = await fetchData<Account>(url, 'account')
  data.account_activity = annotateAccountRecords(data.account_activity)
  return data
}

export const accountQueryOptions = (eventId: string, accountId: string) =>
  queryOptions({
    queryKey: ['events', eventId, 'account', accountId],
    queryFn: async () => fetchAccount(eventId, accountId)
  })

export const useAccountSuspense = (eventId: string, accountId: string) => {
  const { data } = useSuspenseQuery(accountQueryOptions(eventId, accountId))
  return data
}
