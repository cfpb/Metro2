function get(id: string) {
  return cy.findByTestId(id)
}

describe('Basic flow', () => {
  it('Should render the home page view', () => {
    cy.visit('/')

    get('heading').should('have.text', 'Here is your events list')
  })
})
