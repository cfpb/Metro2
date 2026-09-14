import { WellContainer } from '@cfpb/design-system-react'
import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import Table from '@src/components/Table/Table'
import { useEventSuspense } from '@src/queries/event'
import { formatDateRange } from '@src/utils/formatDates'
import { formatNumber } from '@src/utils/formatNumbers'
import { getRouteApi, Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import EventDownloader from './components/EventDownloader'
import getColumnDefinitions from './utils/getColDefs'

export default function EventPage(): ReactElement {
  const { eventId } = getRouteApi('/events/$eventId').useParams()
  const data = useEventSuspense(eventId)
  const dateRange = formatDateRange(
    data.date_range_start,
    data.date_range_end,
    'text'
  )
  return (
    <>
      <LocatorBar heading={data.name} icon='bank-round'>
        <>
          {dateRange ? <div>Data from {dateRange}</div> : null}
          {Number.isNaN(data.total_tradelines) ? null : (
            <div>
              Total tradelines evaluated: {formatNumber(data.total_tradelines)}
            </div>
          )}
        </>
      </LocatorBar>
      <div className='block block--sub'>
        <div className='row'>
          <WellContainer
            data-testid='account-search-container'
            className='account-search-container'>
            <h3>Find an account</h3>
            <p>
              {`Our new account search lets you enter the account number of the account, or accounts, that you're looking for. Then, you can either view the account data or download the results.`}{' '}
            </p>
            <Link
              to='/events/$eventId/accounts'
              params={{ eventId }}
              data-testid='account-search-link'>
              Try the new account search
            </Link>
          </WellContainer>
        </div>
        <div className='row row--action u-mt45'>
          <h2 className='u-mb0'>Evaluator results</h2>
          <EventDownloader rows={data.evaluators} eventName={data.name} />
        </div>
        <div className='row row--content'>
          <Table
            defaultSort={['id']}
            rows={data.evaluators}
            columnDefinitions={getColumnDefinitions(eventId)}
            height='full'
            resizableColumns={false}
          />
        </div>
      </div>
    </>
  )
}
