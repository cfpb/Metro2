import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import LandingPage from 'pages/Landing/LandingPage'

describe('<LandingPage />', () => {
	it('renders Landing page', async () => {
		renderWithProviders(<LandingPage/>)
		expect(await screen.findByText('Here is your events list')).toBeVisible()
	})
})
