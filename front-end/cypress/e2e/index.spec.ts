function get(id: string) {
	return cy.findByTestId(id)
}

describe('Basic flow', () => {
	it('Should render the results view', () => {
		cy.visit('/')

		get('header').should('have.text', 'Results')
	})
})
