import { Link } from '@tanstack/react-router'
import type { EventMetadata } from 'pages/Event/Event'
import type { ReactElement } from 'react'
import './EventList.less'

interface EventListProperties {
  heading: string
  events: EventMetadata[]
}

export default function EventList({
  heading,
  events
}: EventListProperties): ReactElement {
  return (
    <div className='content-row block u-mt15'>
      {/* <h2 className='h5' data-testid='event-heading'>
        {heading}
      </h2> */}
      {events.map(event => (
        <div
          key={event.id}
          className='m-list_item event-item'
          data-testid='event-item'>
          {event.start_date && event.end_date ? (
            <h3 data-testid='event-header'>
              {event.name} - {event.start_date} - {event.end_date}
            </h3>
          ) : (
            <h3 data-testid='event-header'>{event.name}</h3>
          )}
          <h4>Data from:</h4>
          {event.description ? (
            <h4 data-testid='event-description'>{event.description}</h4>
          ) : null}
          <p>
            <Link
              to='/events/$eventId'
              params={{ eventId: String(event.id) }}
              className='m-list-link'>
              Open evaluator results
            </Link>
          </p>
        </div>
      ))}
    </div>
  )
}
