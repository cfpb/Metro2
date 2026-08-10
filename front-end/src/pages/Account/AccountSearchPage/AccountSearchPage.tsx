import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import AccountSearchBar from '@src/pages/Account/AccountSearchPage/components/AccountSearchBar'
import AccountSearchResults from '@src/pages/Account/AccountSearchPage/components/AccountSearchResults'
import { AccountSearchSchema } from '@src/pages/Account/AccountSearchPage/utils/accountSearchSchema'
import { useEventSuspense } from '@src/queries/event'
import { customStringify } from '@src/utils/customStringify'
import { formatDateRange } from '@src/utils/formatDates'
import { getRouteApi, useSearch } from '@tanstack/react-router'
import { type ReactElement } from 'react'

export default function AccountSearchPage(): ReactElement {
  const { cons_acct_num }: AccountSearchSchema = useSearch({ strict: false })
  const accountString = customStringify(cons_acct_num)
  const ids =
    accountString.length > 0 && !Array.isArray(cons_acct_num)
      ? [cons_acct_num]
      : cons_acct_num
  const noSearchTerms =
    accountString === '' || cons_acct_num === undefined || cons_acct_num === null

  // Get event data
  const { eventId } = getRouteApi('/events/$eventId/accounts').useParams()
  const eventData = useEventSuspense(eventId)

  const dateRange = formatDateRange(
    eventData.date_range_start,
    eventData.date_range_end,
    'text'
  )

  return (
    <>
      <LocatorBar
        subhead={`Data from ${eventData.name} ${dateRange ? `from ${dateRange}` : undefined}`}
        heading='Account search'
        breadcrumbs={[
          {
            to: `/events/${String(eventData.id)}`,
            label: 'Event results'
          }
        ]}
      />
      <div className='loader__wrapper'>
        <div className='row row--content row--summary u-mt0'>
          <div className='u-mt30'>
            <AccountSearchBar initialValue={accountString} eventId={eventData.id} />
          </div>
        </div>

        {noSearchTerms ? null : (
          <AccountSearchResults
            accountIds={ids as (string | number)[]}
            eventId={eventData.id}
          />
        )}
      </div>
    </>
  )
}
