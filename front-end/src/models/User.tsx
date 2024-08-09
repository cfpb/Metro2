import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import type { EventMetadata } from 'pages/Event/Event'
import { fetchData } from 'utils/utils'

export default interface User {
  is_admin: boolean
  username: string
  assigned_events: EventMetadata[]
}

export const fetchUser = async (): Promise<User> =>
  fetchData<User>('/api/users/', 'user')

export const userQueryOptions = (): UseQueryOptions<User, Error, User, string[]> =>
  queryOptions({
    queryKey: ['users'],
    queryFn: async () => fetchUser()
  })
