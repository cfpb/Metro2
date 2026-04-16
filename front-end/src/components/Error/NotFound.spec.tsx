import renderWithProviders from '@src/testUtils'
import { screen, within } from '@testing-library/react'
import { notFoundErrors } from './ErrorList'
import NotFoundMessage from './NotFound'

const accountErrorHeading = notFoundErrors.account.title
const defaultErrorHeading = notFoundErrors.event.title
const evaluatorErrorHeading = notFoundErrors.evaluator.title

describe('<NotFoundMessage />', () => {
  it('renders', async () => {
    renderWithProviders(<NotFoundMessage isNotFound={true} routeId='/' />)
    expect(await screen.findByTestId('error-message')).toBeVisible()
  })

  it('should display error title', async () => {
    renderWithProviders(<NotFoundMessage isNotFound={true} routeId='/' />)
    expect(await screen.findByTestId('error-title')).toBeVisible()
  })

  it('should display error description', async () => {
    renderWithProviders(<NotFoundMessage isNotFound={true} routeId='/' />)
    expect(await screen.findByTestId('error-description')).toBeVisible()
  })

  it('should contain button back to homepage', async () => {
    renderWithProviders(<NotFoundMessage isNotFound={true} routeId='/' />)
    expect(await screen.findByTestId('back-button')).toHaveAttribute('href', '/')
  })

  it('displays correct heading for a general 404', async () => {
    renderWithProviders(<NotFoundMessage isNotFound={true} routeId='/' />)
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      defaultErrorHeading
    )
  })

  it('displays correct heading if data prop is random', async () => {
    renderWithProviders(
      <NotFoundMessage isNotFound={true} routeId='/' data='not an error type' />
    )
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      defaultErrorHeading
    )
  })

  it('displays correct heading for a not found event', async () => {
    renderWithProviders(
      <NotFoundMessage isNotFound={true} routeId='/' data='event' />
    )
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      defaultErrorHeading
    )
  })

  it('displays correct heading for a not found evaluator', async () => {
    renderWithProviders(
      <NotFoundMessage isNotFound={true} routeId='/' data='evaluator' />
    )
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      evaluatorErrorHeading
    )
  })

  it('displays correct heading for a not found account', async () => {
    renderWithProviders(
      <NotFoundMessage isNotFound={true} routeId='/' data='account' />
    )
    const element = await screen.findByTestId('error-message')
    expect(within(element).getByTestId('error-title')).toHaveTextContent(
      accountErrorHeading
    )
  })
})
