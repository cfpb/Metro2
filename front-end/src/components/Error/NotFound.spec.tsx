import { screen, within } from '@testing-library/react'
import renderWithProviders from '../../testUtils'
import NotFound from './NotFound'

describe('<NotFound />', () => {
  it('renders', async () => {
    renderWithProviders(<NotFound />)
    expect(await screen.findByTestId('error-message')).toBeVisible()
  })

  it('should display error title', async () => {
    renderWithProviders(<NotFound />)
    expect(await screen.findByTestId('error-title')).toBeVisible()
  })

  it('should display error description', async () => {
    renderWithProviders(<NotFound />)
    expect(await screen.findByTestId('error-description')).toBeVisible()
  })

  it('should contain button back to homepage', async () => {
    renderWithProviders(<NotFound />)
    expect(await screen.findByTestId('back-button')).toHaveAttribute('href', '/')
  })

  it('displays correct title and mailto for a general 404', async () => {
    renderWithProviders(<NotFound />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'The page doesn’t exist.'
    )
  })

  it('displays correct title and mailto for a not found event', async () => {
    renderWithProviders(<NotFound data={{ data: 'event' }} />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'The page doesn’t exist.'
    )
  })

  it('displays correct title and mailto for a not found evaluator', async () => {
    renderWithProviders(<NotFound data={{ data: 'evaluator' }} />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'The results for this evaluator don’t exist.'
    )
  })

  it('displays correct title and mailto for a not found account', async () => {
    renderWithProviders(<NotFound data={{ data: 'account' }} />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'The account doesn’t exist.'
    )
  })
})
