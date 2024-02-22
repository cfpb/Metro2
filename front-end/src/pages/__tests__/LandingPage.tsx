import { render, screen } from '@testing-library/react'
import LandingPage from 'pages/Landing/LandingPage'

describe('<LandingPage />', () => {
	it('renders', () => {
		render(<LandingPage />)
		expect(screen.getByText('Landing page')).toBeInTheDocument()
	})
})
