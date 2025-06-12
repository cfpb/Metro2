import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import EvaluatorPage from './EvaluatorPage'

describe.skip('<EvaluatorPage />', () => {
  it('renders Evaluator page', async () => {
    renderWithProviders(<EvaluatorPage />)
    expect(await screen.findByText('Evaluator')).toBeVisible()
  })
})
