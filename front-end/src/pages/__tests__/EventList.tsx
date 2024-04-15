import { screen, within } from '@testing-library/react'
import EventList from 'pages/Landing/EventList'
import renderWithProviders from '../../testUtils'

const events = [
  {
    id: 1,
    name: 'Bank A Auto Exam',
    start_date: 'January 1, 2018',
    end_date: 'January 1, 2021',
    description: '10 inconsistencies'
  },
  {
    id: 2,
    name: 'Bank B Mortgage Exam'
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

  it('renders an event with dates and description', async () => {
    renderWithProviders(<EventList heading='Test events' events={events} />)
    const eventItems = await screen.findAllByTestId('event-item')
    expect(eventItems).toHaveLength(2)
    const header = within(eventItems[0]).queryByTestId('event-header')
    expect(header).toBeVisible()
    expect(header).toHaveTextContent(
      'Bank A Auto Exam - January 1, 2018 - January 1, 2021'
    )
    const description = within(eventItems[0]).queryByTestId('event-description')
    expect(description).toBeVisible()
    expect(description).toHaveTextContent('10 inconsistencies')
  })

  it('renders an event without dates or description', async () => {
    renderWithProviders(<EventList heading='Test events' events={events} />)
    const eventItems = await screen.findAllByTestId('event-item')
    const header = within(eventItems[1]).queryByTestId('event-header')
    expect(header).toBeVisible()
    expect(header).toHaveTextContent('Bank B Mortgage Exam')
    const description = within(eventItems[1]).queryByTestId('event-description')
    expect(description).not.toBeInTheDocument()
  })
})
