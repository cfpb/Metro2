import { screen } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import { Breadcrumbs } from '../LocatorBar/Breadcrumbs'

describe('<Breadcrumbs />', () => {
  it('displays breadcrumb', async () => {
    renderWithProviders(
      <Breadcrumbs links={[{ href: '', text: 'Back to event results' }]} />
    )
    expect(await screen.findByText(/Back to event results/)).toBeVisible()
  })
})
