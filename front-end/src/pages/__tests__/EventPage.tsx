import { render, screen } from '@testing-library/react'
import EventPage from 'pages/Event/EventPage'

describe('<EventPage />', () => {
	it('renders', () => {
		render(<EventPage />)
		expect(screen.getByText('Event page')).toBeInTheDocument()
	})
})
