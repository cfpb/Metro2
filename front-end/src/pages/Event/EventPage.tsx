import LocatorBar from '@src/components/LocatorBar/LocatorBar'
import Table from '@src/components/Table/Table'
import type Event from '@src/types/Event'
import { formatDateRange } from '@src/utils/formatDates'
import { useLoaderData } from '@tanstack/react-router'
import type { ReactElement } from 'react'
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
      <div className='block block--sub'>
        <div className='row row--right'>
          <EventDownloader rows={eventData.evaluators} eventName={eventData.name} />
        </div>
        <div className='row row--content'>
          <Table
            defaultSort={['id']}
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
