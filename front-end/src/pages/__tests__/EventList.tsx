import { screen, within } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import EventList from 'pages/Landing/EventList'

const events = [
	{
		"id": 1,
		"name": "Bank A Auto Exam",
		"start_date": "January 1, 2018",
		"end_date": "January 1, 2021",
		"description": "10 inconsistencies"
	},
	{
		"id": 2,
		"name": "Bank B Mortgage Exam",
		"start_date": "October 1, 2020",
		"end_date": "October 1, 2022",
		"description": "8 high risk inconsistencies"
	}
]

describe('<EventList />', () => {
	it('renders an event list', async () => {
		renderWithProviders(<EventList heading='Test events' events={ events }/>)
		const eventHeading = await screen.findByTestId('event-heading')
		const eventItems = await screen.findAllByTestId('event-item')
		expect(eventHeading).toHaveTextContent('Test events')
		expect(eventItems).toHaveLength(2)
		expect(within(eventItems[0]).getByText(/Bank A Auto Exam/)).toBeVisible()
		expect(within(eventItems[0]).getByText(/January 1, 2018/)).toBeVisible()
		expect(within(eventItems[0]).getByText(/January 1, 2021/)).toBeVisible()
		expect(within(eventItems[0]).getByText(/10 inconsistencies/)).toBeVisible()
	})
})
