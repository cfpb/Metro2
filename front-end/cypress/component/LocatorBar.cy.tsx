import LocatorBar from '@src/components/LocatorBar/LocatorBar'
describe('LocatorBar.cy.tsx', () => {
  it('displays a single heading', () => {
    cy.mount(<LocatorBar icon='bank-round' heading='Home page' />)
    cy.findByTestId('locator-bar-icon')
      .should('be.visible')
      .find('svg')
      .should('be.visible')
      .and('have.attr', 'alt', 'bank-round')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Home page')
    cy.findByTestId('locator-bar-eyebrow').should('not.exist')
    cy.findByTestId('locator-bar-subhead').should('not.exist')
  })

  it('displays multiple headings', () => {
    cy.mount(
      <LocatorBar
        icon='bank-round'
        heading='Test-Eval-1'
        eyebrow='Evaluator'
        subhead='Short description of evaluator'
      />
    )
    cy.findByTestId('locator-bar-icon')
      .should('be.visible')
      .find('svg')
      .should('be.visible')
      .and('have.attr', 'alt', 'bank-round')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Test-Eval-1')
    cy.findByTestId('locator-bar-eyebrow')
      .should('be.visible')
      .and('have.text', 'Evaluator')
    cy.findByTestId('locator-bar-subhead')
      .should('be.visible')
      .and('have.text', 'Short description of evaluator')
  })

  it('displays breadcrumbs', () => {
    cy.mountWithProviders(
      <LocatorBar
        icon='bank-round'
        heading='Home page'
        breadcrumbs={[{ href: '/results', text: 'Back to results' }]}
      />
    )
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Home page')
    cy.get('.m-breadcrumbs').should('be.visible')
  })
})
