import { useNavigate, useSearch } from '@tanstack/react-router'
import { screen } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

import renderWithProviders from '../../../../testUtils'
import EvaluatorResultsTabs from './ResultsTabbedNavigation'

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
    renderWithProviders(<EvaluatorResultsTabs />)
    const sampleTab = await screen.findByTestId('sample-results-tab')
    const allTab = await screen.findByTestId('all-results-tab')

    expect(sampleTab).not.toHaveClass('active')
    expect(allTab).toHaveClass('active')
  })

  it('sample results button is checked when useSearch returns sample', async () => {
    vi.mocked(useSearch).mockReturnValue('sample')
    renderWithProviders(<EvaluatorResultsTabs />)
    const sampleTab = await screen.findByTestId('sample-results-tab')
    const allTab = await screen.findByTestId('all-results-tab')

    expect(sampleTab).toHaveClass('active')
    expect(allTab).not.toHaveClass('active')
  })

  it('navigate is called when toggle radio is clicked', async () => {
    vi.mocked(useSearch).mockReturnValue('sample')
    vi.mocked(useNavigate).mockImplementation(() => mocks.navigate)
    renderWithProviders(<EvaluatorResultsTabs />)
    const sampleTab = await screen.findByTestId('sample-results-tab')
    const allTab = await screen.findByTestId('all-results-tab')
    // on load, sample button should be checked
    expect(sampleTab).toHaveClass('active')
    expect(allTab).not.toHaveClass('active')
    expect(mocks.navigate).not.toBeCalled()
    // clicking the all button should call navigate
    allTab.click()
    expect(mocks.navigate).toBeCalledTimes(1)
  })
})
