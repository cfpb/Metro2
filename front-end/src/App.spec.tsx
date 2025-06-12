import { screen } from '@testing-library/react'
import App from 'App'
import renderWithProviders from 'testUtils'

describe.skip('<App />', () => {
  it('renders', async () => {
    window.history.pushState({}, 'Home', '/')
    renderWithProviders(<App />)
    expect(await screen.findByText('Metro2 Evaluator Tool')).toBeVisible()
  })
})
