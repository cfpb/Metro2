import { screen } from '@testing-library/react'
import EventPage from 'pages/Event/EventPage'
import renderWithProviders from '../../testUtils'

describe.skip('<EventPage />', () => {
  it('renders Event page', async () => {
    // await act(() => renderWithProviders(<EventPage />))
    renderWithProviders(<EventPage />)
    expect(await screen.findByText('Sample-Dataset-007')).toBeVisible()
  })
})
