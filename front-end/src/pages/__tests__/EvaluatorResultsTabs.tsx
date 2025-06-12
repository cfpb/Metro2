import { useNavigate, useSearch } from '@tanstack/react-router'
import { screen } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

import EvaluatorResultsToggle from 'pages/Evaluator/results/components/ResultsToggle'
import renderWithProviders from '../../testUtils'

const mocks = vi.hoisted(() => ({
  useNavigate: vi.fn(),
  navigate: vi.fn()
}))

vi.mock('@tanstack/react-router', async () => {
  const actual: object = await vi.importActual('@tanstack/react-router')
  return {
    ...actual,
    useSearch: vi.fn(),
    useNavigate: mocks.useNavigate
  }
})

describe('<EvaluatorResultsToggle />', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('all results button is checked when useSearch returns all', async () => {
    vi.mocked(useSearch).mockReturnValue('all')
    renderWithProviders(<EvaluatorResultsToggle />)
    const sampleButton = await screen.findByTestId('sample-results-button')
    const allButton = await screen.findByTestId('all-results-button')

    expect(sampleButton).not.toHaveClass('active')
    expect(allButton).toHaveClass('active')
  })

  it('sample results button is checked when useSearch returns sample', async () => {
    vi.mocked(useSearch).mockReturnValue('sample')
    renderWithProviders(<EvaluatorResultsToggle />)
    const sampleButton = await screen.findByTestId('sample-results-button')
    const allButton = await screen.findByTestId('all-results-button')

    expect(sampleButton).toHaveClass('active')
    expect(allButton).not.toHaveClass('active')
  })

  it('navigate is called when toggle radio is clicked', async () => {
    vi.mocked(useSearch).mockReturnValue('sample')
    vi.mocked(useNavigate).mockImplementation(() => mocks.navigate)
    renderWithProviders(<EvaluatorResultsToggle />)
    const sampleButton = await screen.findByTestId('sample-results-button')
    const allButton = await screen.findByTestId('all-results-button')
    // on load, sample button should be checked
    expect(sampleButton).toHaveClass('active')
    expect(allButton).not.toHaveClass('active')
    expect(mocks.navigate).not.toBeCalled()
    // clicking the all button should call navigate
    allButton.click()
    expect(mocks.navigate).toBeCalledTimes(1)
  })
})
