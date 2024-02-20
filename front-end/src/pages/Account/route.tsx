import { createRoute } from '@tanstack/react-router'
import { eventRoute } from '../Event/route'
import AccountPage from './AccountPage'

const accountRoute = createRoute( {
  path: '/accounts/$accountId',
  getParentRoute: () => eventRoute,
  component: AccountPage
} )

export default accountRoute