import renderWithProviders from '@src/testUtils'
import { screen } from '@testing-library/react'
import { Breadcrumbs } from './Breadcrumbs'

describe('<Breadcrumbs />', () => {
  it('displays breadcrumb', async () => {
    renderWithProviders(
      <Breadcrumbs links={[{ href: '', text: 'Back to event results' }]} />
    )
    expect(await screen.findByText(/Back to event results/)).toBeVisible()
  })
})
