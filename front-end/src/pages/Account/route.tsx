import { accountPageSchema } from '@src/pages/Account/AccountPage/utils/accountSchema'
import { accountSearchSchema } from '@src/pages/Account/AccountSearchPage/utils/accountSearchSchema'
import { eventRoute } from '@src/pages/Event/route'
import { accountQueryOptions } from '@src/queries/account'
import { createRoute } from '@tanstack/react-router'
import AccountPage from './AccountPage/AccountPage'
import AccountSearchPage from './AccountSearchPage/AccountSearchPage'

export const accountsRoute = createRoute({
  getParentRoute: () => eventRoute,
  path: 'accounts'
})

export const accountSearchRoute = createRoute({
  path: '/',
  getParentRoute: () => accountsRoute,
  validateSearch: accountSearchSchema,
  component: AccountSearchPage
})

export const accountRoute = createRoute({
  path: '/$accountId',
  getParentRoute: () => accountsRoute,
  component: AccountPage,
  validateSearch: accountPageSchema,
  loader: async ({ context: { queryClient }, params: { eventId, accountId } }) => {
    const options = accountQueryOptions(eventId, accountId)
    return queryClient.ensureQueryData(options)
  }
})
