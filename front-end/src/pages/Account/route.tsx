import { accountSchema } from '@src/pages/Account/utils/accountSearchSchema'
import { eventRoute } from '@src/pages/Event/route'
import { accountQueryOptions } from '@src/queries/account'
import { createRoute } from '@tanstack/react-router'
import AccountPage from './AccountPage'

const accountRoute = createRoute({
  path: '/accounts/$accountId',
  getParentRoute: () => eventRoute,
  component: AccountPage,
  validateSearch: accountSchema,
  loader: async ({ context: { queryClient }, params: { eventId, accountId } }) => {
    const options = accountQueryOptions(eventId, accountId)
    return queryClient.ensureQueryData(options)
  }
})

export default accountRoute
