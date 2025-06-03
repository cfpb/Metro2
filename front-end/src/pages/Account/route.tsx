import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { createRoute } from '@tanstack/react-router'
import { annotateAccountRecords, fetchData } from 'utils/utils'
import { eventRoute } from '../Event/route'
import type Account from './Account'
import AccountPage from './AccountPage'

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

const accountRoute = createRoute({
  path: '/accounts/$accountId',
  getParentRoute: () => eventRoute,
  component: AccountPage,
  loader: async ({ context: { queryClient }, params: { eventId, accountId } }) => {
    const options = accountQueryOptions(eventId, accountId)
    return queryClient.ensureQueryData(options)
  }
})

export default accountRoute
