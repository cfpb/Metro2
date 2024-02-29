import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import EventPage from 'pages/Event/EventPage'

describe('<EventPage />', () => {
	it('renders Event page', async () => {
		renderWithProviders(<EventPage/>)
		expect(await screen.findByText('Test bank exam')).toBeVisible()
	})
})
