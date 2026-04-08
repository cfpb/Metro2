import type User from '@src/types/User'
import fetchData from '@src/utils/fetchData'
import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'

export const fetchUser = async (): Promise<User> =>
  fetchData<User>('/api/users/', 'user')

export const userQueryOptions = (): UseQueryOptions<User, Error, User, string[]> =>
  queryOptions({
    queryKey: ['users'],
    queryFn: async () => fetchUser()
  })
