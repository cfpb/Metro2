import { render, screen } from '@testing-library/react'
import LocatorBar from './LocatorBar'

describe('<LocatorBar />', () => {
  it('displays a single heading', () => {
    render(<LocatorBar heading='Home page' icon='bank-round' />)
    expect(screen.getByText('Home page')).toBeInTheDocument()
    expect(screen.queryByTestId('locator-bar-eyebrow')).not.toBeInTheDocument()
    expect(screen.queryByTestId('locator-bar-subhead')).not.toBeInTheDocument()
  })

  it('displays all headings', () => {
    render(
      <LocatorBar
        heading='Test-Eval-1'
        eyebrow='Evaluator'
        icon='bank-round'
        subhead='Short description of evaluator'
      />
    )
    expect(screen.getByText('Test-Eval-1')).toBeInTheDocument()
    expect(screen.getByText('Evaluator')).toBeInTheDocument()
    expect(screen.getByText('Short description of evaluator')).toBeInTheDocument()
  })
})
