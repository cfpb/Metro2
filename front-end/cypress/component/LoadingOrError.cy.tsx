import LoadingOrError from '@src/components/LoadingOrError/LoadingOrError'

describe('LoadingOrError', () => {
  it('renders', () => {
    cy.mount(<LoadingOrError />)
    cy.findByTestId('loader').should('be.visible')
  })

  it('renders with an error message', () => {
    cy.mount(<LoadingOrError error={new Error('Failed to fetch')} />)
    cy.findByText('Failed to fetch').should('be.visible')
  })
})
