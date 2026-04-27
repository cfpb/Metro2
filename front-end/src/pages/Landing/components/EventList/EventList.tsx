import type EventMetadata from '@src/types/EventMetadata'
import { formatDateRange } from '@src/utils/formatDates'
import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './EventList.scss'

interface EventListProperties {
  events: EventMetadata[]
}

export default function EventList({ events }: EventListProperties): ReactElement {
  return (
    <div className='row row--content block u-mt15'>
      <h2>Your events</h2>
      {events.map(event => (
        <div
          key={event.id}
          className='m-list_item event-item'
          data-testid='event-item'>
          <h3 data-testid='event-header'>
            <Link
              to='/events/$eventId'
              params={{ eventId: String(event.id) }}
              className='m-list-link'
              data-testid='event-link'>
              {event.name}
              {event.eid_or_matter_num
                ? `: EID/Matter #${event.eid_or_matter_num}`
                : null}
            </Link>
          </h3>
          <h4 data-testid='event-date-range'>
            Data from:{' '}
            {formatDateRange(event.date_range_start, event.date_range_end, 'text')}
          </h4>
        </div>
      ))}
    </div>
  )
}
