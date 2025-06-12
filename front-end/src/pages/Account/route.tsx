import { createRoute } from '@tanstack/react-router'
import { accountQueryOptions } from 'queries/account'
import { eventRoute } from '../Event/route'
import AccountPage from './AccountPage'

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
