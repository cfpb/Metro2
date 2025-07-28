import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type Event from 'types/Event'
import { formatDateRange } from 'utils/formatDates'
import EventDownloader from './components/EventDownloader'
import getColumnDefinitions from './utils/getColDefs'

export default function EventPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const dateRange = formatDateRange(
    eventData.date_range_start,
    eventData.date_range_end,
    'text'
  )
  return (
    <>
      <LocatorBar
        heading={eventData.name}
        icon='bank-round'
        subhead={dateRange ? `Data from ${dateRange}` : undefined}
      />
      <div className='block block__sub'>
        <div className='row row__action'>
          <EventDownloader rows={eventData.evaluators} eventName={eventData.name} />
        </div>
        <div className='row row__content'>
          <Table
            rows={eventData.evaluators}
            columnDefinitions={getColumnDefinitions(String(eventData.id))}
            height='full'
            resizableColumns={false}
          />
        </div>
      </div>
    </>
  )
}
