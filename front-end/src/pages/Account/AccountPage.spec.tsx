import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import AccountPage from './AccountPage'

describe.skip('<AccountPage />', () => {
  it('renders Account page', async () => {
    renderWithProviders(<AccountPage />)
    expect(await screen.findByText('Account')).toBeVisible()
  })
})
