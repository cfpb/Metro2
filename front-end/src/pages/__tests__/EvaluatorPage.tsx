import { render, screen } from '@testing-library/react'
import EvaluatorPage from 'pages/Evaluator/EvaluatorPage'

describe('<EvaluatorPage />', () => {
	it('renders', () => {
		render(<EvaluatorPage />)
		expect(screen.getByText('Evaluator page')).toBeInTheDocument()
	})
})
