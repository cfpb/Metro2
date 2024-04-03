import { screen } from '@testing-library/react'
import AccountPage from 'pages/Account/AccountPage'
import renderWithProviders from '../../testUtils'

describe.skip('<AccountPage />', () => {
  it('renders Account page', async () => {
    renderWithProviders(<AccountPage />)
    expect(await screen.findByText('Account')).toBeVisible()
  })
})
