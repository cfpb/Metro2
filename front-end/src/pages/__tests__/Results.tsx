import { render, screen } from '@testing-library/react'
import ResultsPage from 'pages/Results'

describe('<Results />', () => {
	it('renders', () => {
		render(<ResultsPage />)
		expect(screen.getByText('Results')).toBeInTheDocument()
	})
})
