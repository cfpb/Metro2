import { screen } from '@testing-library/react'
import EventPage from 'pages/Event/EventPage'
import renderWithProviders from '../../testUtils'

describe.skip('<EventPage />', () => {
  it('renders Event page', async () => {
    renderWithProviders(<EventPage />)
    expect(await screen.findByText('Bank A auto exam')).toBeVisible()
  })
})
