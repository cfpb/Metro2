import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'

import type EventMetadata from 'types/EventMetadata'
import { formatDateRange } from 'utils/formatDates'
import './EventList.less'

interface EventListProperties {
  heading?: string
  events: EventMetadata[]
}

export default function EventList({
  heading,
  events
}: EventListProperties): ReactElement {
  return (
    <div className='row row__content block u-mt15'>
      {heading ? (
        <h2 className='h5' data-testid='event-heading'>
          {heading}
        </h2>
      ) : null}
      {events.map(event => (
        <div
          key={event.id}
          className='m-list_item event-item'
          data-testid='event-item'>
          <h3 data-testid='event-header'>
            {event.name}
            {event.eid_or_matter_num
              ? `: EID/Matter #${event.eid_or_matter_num}`
              : null}
          </h3>
          <h4 data-testid='event-date-range'>
            Data from:{' '}
            {formatDateRange(event.date_range_start, event.date_range_end, 'text')}
          </h4>
          <p>
            <Link
              to='/events/$eventId'
              params={{ eventId: String(event.id) }}
              className='m-list-link'
              data-testid='event-link'>
              Open evaluator results
            </Link>
          </p>
        </div>
      ))}
    </div>
  )
}
