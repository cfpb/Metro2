import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import LandingPage from './LandingPage'

describe.skip('<LandingPage />', () => {
  it('renders Landing page', async () => {
    renderWithProviders(<LandingPage />)
    expect(await screen.findByText('Here is your events list')).toBeVisible()
  })
})
