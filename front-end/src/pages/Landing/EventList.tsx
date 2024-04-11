import type { ReactElement } from 'react'
import { Link } from '@tanstack/react-router'
import './EventList.less'

interface Event {
  id: number
  name: string
  start_date: string
  end_date: string
  description: string
}

interface EventListProperties {
  heading: string
  events: Event[]
}

export default function EventList({
  heading,
  events
}: EventListProperties): ReactElement {
  return (
    <div className='content-row block u-mt15'>
      <h2 className='h5' data-testid='event-heading'>
        {heading}
      </h2>
      {events.map(event => (
        <div
          key={event.id}
          className='m-list_item event-item'
          data-testid='event-item'>
          <h3>
            {event.name} - {event.start_date} - {event.end_date}
          </h3>
          <h4>{event.description}</h4>
          <Link
            to='/events/$eventId'
            params={{ eventId: String(event.id) }}
            className='m-list-link'>
            View event results
          </Link>
        </div>
      ))}
    </div>
  )
}
