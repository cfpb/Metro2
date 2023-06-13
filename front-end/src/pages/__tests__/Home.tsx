import { render, screen } from '@testing-library/react'
import HomePage from 'pages/Home'

describe('<HomePage />', () => {
	it('renders', () => {
		render(<HomePage />)
		expect(screen.getByText('Your cases')).toBeInTheDocument()
	})
})
