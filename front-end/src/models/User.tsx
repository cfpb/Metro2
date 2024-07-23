import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import type { EventMetadata } from 'pages/Event/Event'
import { fetchData } from 'utils/utils'

export default interface User {
  is_admin: boolean
  username: string
  assigned_events: EventMetadata[]
}

export const fetchUser = async (): Promise<User> => {
  // Set url based on environment
  // In dev, add id param for admin user created in setup script
  // In production, /users/ without an id returns data for logged in user
  const url = import.meta.env.DEV ? '/api/users/1/' : '/api/users/'
  return fetchData<User>(url, 'user')
}

export const userQueryOptions = (): UseQueryOptions<User, Error, User, string[]> =>
  queryOptions({
    queryKey: ['users'],
    queryFn: async () => fetchUser()
  })
