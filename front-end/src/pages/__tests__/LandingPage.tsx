import { screen } from '@testing-library/react'
import LandingPage from 'pages/Landing/LandingPage'
import renderWithProviders from '../../testUtils'

describe.skip('<LandingPage />', () => {
  it('renders Landing page', async () => {
    renderWithProviders(<LandingPage />)
    expect(await screen.findByText('Here is your events list')).toBeVisible()
  })
})
