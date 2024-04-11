import { screen } from '@testing-library/react'
import EvaluatorPage from 'pages/Evaluator/EvaluatorPage'
import renderWithProviders from '../../testUtils'

describe.skip('<EvaluatorPage />', () => {
  it('renders Evaluator page', async () => {
    renderWithProviders(<EvaluatorPage />)
    expect(await screen.findByText('Inconsistency')).toBeVisible()
  })
})
