import renderWithProviders from '@src/testUtils'
import { screen } from '@testing-library/react'
import AccountPage from './AccountPage'

describe.skip('<AccountPage />', () => {
  it('renders Account page', async () => {
    renderWithProviders(<AccountPage />)
    expect(await screen.findByText('Account')).toBeVisible()
  })
})
