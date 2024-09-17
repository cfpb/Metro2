import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import { formatDate } from 'utils/formatters'
import type Event from './Event'
import EventDownloader from './EventDownloader'
import getColumnDefinitions from './columnDefinitions'

export default function EventPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  return (
    <>
      <LocatorBar
        heading={eventData.name}
        icon='bank-round'
        subhead={
          eventData.date_range_start && eventData.date_range_end
            ? `Data from ${formatDate(
                eventData.date_range_start,
                true
              )} - ${formatDate(eventData.date_range_end, true)}`
            : undefined
        }
      />
      <div className='block block__sub content-row'>
        <div className='download-row'>
          <EventDownloader rows={eventData.evaluators} eventName={eventData.name} />
        </div>
        <Table
          rows={eventData.evaluators}
          columnDefinitions={getColumnDefinitions(String(eventData.id))}
          height='full'
          resizableColumns={false}
        />
      </div>
    </>
  )
}
