import { createRoute } from '@tanstack/react-router'
import { userQueryOptions } from 'models/User'
import rootRoute from '../rootRoute'
import LandingPage from './LandingPage'

const indexRoute = createRoute({
  path: '/',
  getParentRoute: () => rootRoute,
  component: LandingPage,
  loader: async ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(userQueryOptions())
})

export default indexRoute
