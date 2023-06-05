import { render, screen } from '@testing-library/react'
import EvaluatorPage from 'pages/Evaluator'

describe('<Evaluator />', () => {
	it('renders', () => {
		render(<EvaluatorPage />)
		expect(screen.getByText('Evaluator')).toBeInTheDocument()
	})
})