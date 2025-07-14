import { useQuery } from '@tanstack/react-query'
import { Icon } from 'design-system-react'
import { accountHolderQueryOptions } from 'queries/accountHolder'
import type { ReactElement } from 'react'
import { useState } from 'react'

interface AccountHolderProperties {
  accountId: string
  eventId: number
}

export default function AccountContactInformation({
  accountId,
  eventId
}: AccountHolderProperties): ReactElement {
  const { data, refetch, isLoading } = useQuery(
    accountHolderQueryOptions(eventId, accountId)
  )
  const [showPII, setShowPII] = useState(false)

  function onClickHandler(): void {
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    if (!data) refetch()
    setShowPII(true)
  }

  if (isLoading) {
    return (
      <div className='inline-loader'>
        <Icon name='updating' />
        Loading...
      </div>
    )
  }

  return data && showPII ? (
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
