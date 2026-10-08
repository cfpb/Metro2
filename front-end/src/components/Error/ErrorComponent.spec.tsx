import renderWithProviders from '@src/testUtils'
import { screen, within } from '@testing-library/react'
import ErrorComponent from './ErrorComponent'

// eslint-disable-next-line @typescript-eslint/no-empty-function
const noop = () => {}

describe('<ErrorComponent />', () => {
  it('renders', async () => {
    renderWithProviders(<ErrorComponent error={new Error('500')} reset={noop} />)
    expect(await screen.findByTestId('error-message')).toBeVisible()
  })

  it('should display error title', async () => {
    renderWithProviders(<ErrorComponent error={new Error('500')} reset={noop} />)
    expect(await screen.findByTestId('error-title')).toBeVisible()
  })

  it('should display error description', async () => {
    renderWithProviders(<ErrorComponent error={new Error('500')} reset={noop} />)
    expect(await screen.findByTestId('error-description')).toBeVisible()
  })

  it('should contain button back to homepage', async () => {
    renderWithProviders(<ErrorComponent error={new Error('500')} reset={noop} />)
    expect(await screen.findByTestId('back-button')).toHaveAttribute('href', '/')
  })

  it('displays correct title and mailto for a 500 error', async () => {
    renderWithProviders(<ErrorComponent error={new Error('500')} reset={noop} />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'Something went wrong.'
    )
  })

  it('displays correct title and mailto for a random error', async () => {
    renderWithProviders(
      <ErrorComponent error={new Error('Internal error message')} reset={noop} />
    )
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'Something went wrong.'
    )
  })

  it('displays correct title and mailto for a 401 error', async () => {
    renderWithProviders(<ErrorComponent error={new Error('401')} reset={noop} />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      'Sorry, we can’t show you this page.'
    )
  })
})
