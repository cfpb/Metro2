import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type Event from './Event'
import columnDefinitions from './columnDefinitions'

export default function EventPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })

  return (
    <>
      <LocatorBar
        heading={eventData.name}
        icon='bank-round'
        subhead={
          eventData.date_range_start && eventData.date_range_end
            ? `Data from ${eventData.date_range_start} - ${eventData.date_range_end}`
            : undefined
        }
      />
      <div className='block block__sub content-row'>
        <Table
          rows={eventData.evaluators}
          columnDefinitions={columnDefinitions}
          height='full'
          resizableColumns={false}
        />
      </div>
    </>
  )
}
