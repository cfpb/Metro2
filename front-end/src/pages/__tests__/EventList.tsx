import { screen, within } from '@testing-library/react'
import EventList from 'pages/Landing/components/EventList/EventList'
import renderWithProviders from '../../testUtils'

const events = [
  {
    id: 1,
    name: 'Bank A Auto Exam',
    date_range_start: '2018-02-18',
    date_range_end: '2021-02-18',
    eid_or_matter_num: '123-456'
  },
  {
    id: 2,
    name: 'Bank B Mortgage Exam',
    date_range_start: '2020-01-01',
    date_range_end: '2022-01-01'
  }
]

describe('<EventList />', () => {
  it('renders an event list', async () => {
    renderWithProviders(<EventList heading='Test events' events={events} />)
    const eventHeading = await screen.findByTestId('event-heading')

    const eventItems = await screen.findAllByTestId('event-item')
    expect(eventHeading).toHaveTextContent('Test events')
    expect(eventItems).toHaveLength(2)
  })

  it('renders an event with dates and eid', async () => {
    renderWithProviders(<EventList heading='Test events' events={events} />)
    const eventItems = await screen.findAllByTestId('event-item')
    expect(eventItems).toHaveLength(2)
    const header = within(eventItems[0]).queryByTestId('event-header')
    expect(header).toBeVisible()
    expect(header).toHaveTextContent('Bank A Auto Exam: EID/Matter #123-456')
    const dateRange = within(eventItems[0]).queryByTestId('event-date-range')
    expect(dateRange).toBeVisible()
    expect(dateRange).toHaveTextContent('Data from: Feb 2018 - Feb 2021')

    const eventLink = within(eventItems[0]).queryByTestId('event-link')
    expect(eventLink).toBeVisible()
    expect(eventLink).toHaveAttribute('href', '/events/1')
  })

  it('renders an event without eid', async () => {
    renderWithProviders(<EventList heading='Test events' events={events} />)
    const eventItems = await screen.findAllByTestId('event-item')
    const header = within(eventItems[1]).queryByTestId('event-header')
    expect(header).toBeVisible()
    expect(header).toHaveTextContent('Bank B Mortgage Exam')
  })
})
