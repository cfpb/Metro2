import renderWithProviders from '@src/testUtils'
import { screen } from '@testing-library/react'
import LandingPage from './LandingPage'

describe.skip('<LandingPage />', () => {
  it('renders Landing page', async () => {
    renderWithProviders(<LandingPage />)
    expect(await screen.findByText('Here are your assigned events')).toBeVisible()
  })
})
