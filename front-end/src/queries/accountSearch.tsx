import type AccountSummary from '@src/types/AccountSummary'
import { annotateM2FieldValue } from '@src/utils/annotations'
import { customStringify } from '@src/utils/customStringify'
import fetchData from '@src/utils/fetchData'
import { queryOptions, useQuery } from '@tanstack/react-query'

export const fetchAccounts = async (
  eventId: string,
  accountIds: string | string[]
): Promise<AccountSummary[] | []> => {
  const searchParam = customStringify(accountIds)
  const url = `/api/events/${eventId}/account/?cons_acct_num=${searchParam}`
  const data = await fetchData<AccountSummary[] | []>(url, 'accounts')
  // Add annotations for portfolio and account type fields
  if (data.length > 0) {
    for (const acct of data) {
      acct.port_type = annotateM2FieldValue('port_type', acct.port_type) as string
      acct.acct_type = annotateM2FieldValue('acct_type', acct.acct_type) as string
    }
  }
  return data
}

export const accountsQueryOptions = (
  eventId: string,
  accountIds: string | string[]
) =>
  queryOptions({
    queryKey: ['events', eventId, 'accounts', accountIds],
    queryFn: async () => fetchAccounts(eventId, accountIds)
  })

export const useAccounts = (eventId: string, accountIds: string | string[]) =>
  useQuery(accountsQueryOptions(eventId, accountIds))
