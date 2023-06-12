function get(id: string) {
	return cy.findByTestId(id)
}

describe('Basic flow', () => {
	it('Should render the home page view', () => {
		cy.visit('/')

		get('header').should('have.text', 'Your cases')
	})
})
