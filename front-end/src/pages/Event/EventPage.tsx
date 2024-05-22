import { useLoaderData } from '@tanstack/react-router'
import LocatorBar from 'components/LocatorBar/LocatorBar'
import Table from 'components/Table/Table'
import type { ReactElement } from 'react'
import type Event from './Event'
import columnDefinitions from './columnDefinitions'
import EventDownloader from './EventDownloader'

export default function EventPage(): ReactElement {
  const eventData: Event = useLoaderData({ from: '/events/$eventId' })
  const fields = ['id', 'description', 'category', 'hits', 'accounts_affected']
  const headerLookup = {id: 'ID', description: 'DESCRIPTION', category: 'CATEGORY', hits: 'HITS', accounts_affected: 'ACCOUNTS AFFECTED'}

  return (
    <>
      <LocatorBar
        heading={eventData.name}
        icon='bank-round'
        subhead={
          eventData.start_date && eventData.end_date
            ? `Data from ${eventData.start_date} - ${eventData.end_date}`
            : undefined
        }
      />
      <div className='block block__sub content-row'>
      <div className='download-row'>
        <EventDownloader fields={fields} rows={eventData.evaluators} headerLookup={headerLookup} eventName={eventData.name}/>
      </div>
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
