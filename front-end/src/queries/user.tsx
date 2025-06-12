import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import fetchData from 'utils/fetchData'
import type User from '../types/User'

export const fetchUser = async (): Promise<User> =>
  fetchData<User>('/api/users/', 'user')

export const userQueryOptions = (): UseQueryOptions<User, Error, User, string[]> =>
  queryOptions({
    queryKey: ['users'],
    queryFn: async () => fetchUser()
  })
