import type { UseQueryOptions } from '@tanstack/react-query'
import { queryOptions } from '@tanstack/react-query'
import { fetchData } from 'utils/utils'

export interface AccountHolder {
  addr_ind: string
  addr_line_1: string
  addr_line_2: string
  city: string
  cons_acct_num: string
  cons_info_ind: string
  country_cd: string
  dob: string
  ecoa: string
  first_name: string
  gen_code: string
  id: string
  middle_name: string
  phone_num: string
  res_cd: string
  ssn: string
  state: string
  surname: string
  zip: string
}

export const ACCOUNT_HOLDER_FIELDS = new Map([
  ['first_name', 'First name'],
  ['middle_name', 'Middle name'],
  ['surname', 'Surname'],
  ['gen_code', 'Generation code'],
  ['addr_line_1', 'Address line 1'],
  ['addr_line_2', 'Address line 2'],
  ['city', 'City'],
  ['state', 'State'],
  ['zip', 'Zip code'],
  ['country_cd', 'Country code'],
  ['phone_num', 'Phone number'],
  ['dob', 'Date of birth'],
  ['ssn', 'Social security number'],
  ['cons_acct_num', 'Consumer account number']
])

export const fetchAccountHolderData = async (
  eventId: number,
  accountId: string
): Promise<AccountHolder> => {
  const url = `/api/events/${eventId}/account/${accountId}/account_holder/`
  return fetchData<AccountHolder>(url, 'account')
}

export const accountHolderQueryOptions = (
  eventId: number,
  accountId: string
): UseQueryOptions<AccountHolder, Error, AccountHolder, (number | string)[]> =>
  queryOptions({
    queryKey: ['event', eventId, 'accountHolder', accountId],
    queryFn: async (): Promise<AccountHolder> =>
      fetchAccountHolderData(eventId, accountId),
    enabled: false,
    staleTime: Number.POSITIVE_INFINITY
  })
