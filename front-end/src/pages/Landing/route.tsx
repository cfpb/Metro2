import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { createRoute } from '@tanstack/react-router'
import { fetchData } from 'utils/utils'
import rootRoute from '../rootRoute'
import LandingPage from './LandingPage'
import type User from './User'

export const fetchUser = async (): Promise<User> => {
  // Set url based on environment
  // In dev, add id param for admin user created in setup script
  // In production, /users/ without an id returns data for logged in user
  const url = import.meta.env.DEV ? '/api/users/1/' : '/api/users/'
  return fetchData<User>(url, 'user')
}

export const userQueryOptions = (): UseQueryOptions<
  User,
  Error,
  unknown,
  string[]
> =>
  queryOptions({
    queryKey: ['users'],
    queryFn: async () => fetchUser()
  })

const indexRoute = createRoute({
  path: '/',
  getParentRoute: () => rootRoute,
  component: LandingPage,
  loader: async ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(userQueryOptions())
})

export default indexRoute
