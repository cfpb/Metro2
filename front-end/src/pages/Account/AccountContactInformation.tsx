import { useQuery } from '@tanstack/react-query'
import { Icon } from 'design-system-react'
import type { ReactElement } from 'react'
import { fetchData } from 'utils/utils'
import type { AccountHolder } from './Account'

interface AccountHolderProperties {
  accountId: string
  eventId: number
}
export const fetchAccountPII = async (
  eventId: number,
  accountId: string
): Promise<AccountHolder> => {
  const url = `/api/events/${eventId}/account/${accountId}/account_holder/`
  return fetchData<AccountHolder>(url, 'account')
}

export default function AccountContactInformation({
  accountId,
  eventId
}: AccountHolderProperties): ReactElement {
  const { data, refetch, isLoading } = useQuery({
    queryKey: ['events', eventId, 'accountPII', accountId],
    queryFn: async (): Promise<AccountHolder> => fetchAccountPII(eventId, accountId),
    enabled: false
  })

  if (isLoading) {
    return (
      <div className='inline-loader'>
        <Icon name='updating' />
        Loading...
      </div>
    )
  }

  function onClickHandler(): void {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    refetch()
  }

  return data ? (
    <div>
      <div>{`${data.first_name} ${data.surname}`}</div>
      <div>{data.addr_line_1}</div>
      <div>{data.addr_line_2}</div>
      <div>{`${data.city}, ${data.state} ${data.zip}`}</div>
      <div>{data.phone_num}</div>
    </div>
  ) : (
    <button className='a-btn a-btn__link' type='button' onClick={onClickHandler}>
      Show
    </button>
  )
}
