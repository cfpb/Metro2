import renderWithProviders from '@src/testUtils'
import { screen } from '@testing-library/react'
import EvaluatorPage from './EvaluatorPage'

describe.skip('<EvaluatorPage />', () => {
  it('renders Evaluator page', async () => {
    renderWithProviders(<EvaluatorPage />)
    expect(await screen.findByText('Evaluator')).toBeVisible()
  })
})
