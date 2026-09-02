import LocatorBar from '@src/components/LocatorBar/LocatorBar'
describe('LocatorBar.cy.tsx', () => {
  it('displays a single heading', () => {
    cy.mount(<LocatorBar icon='bank-round' heading='Home page' />)
    cy.get('.locator-bar')
      .should('be.visible')
      .and('have.class', 'locator-bar--vertically-centered')
    cy.findByTestId('locator-bar-icon')
      .should('be.visible')
      .and('have.class', 'cf-icon-svg--bank-round')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Home page')
    cy.findByTestId('locator-bar-eyebrow').should('not.exist')
    cy.findByTestId('locator-bar-subhead').should('not.exist')
  })

  it('displays multiple headings', () => {
    cy.mount(
      <LocatorBar icon='bank-round' heading='Test-Eval-1' eyebrow='Evaluator' />
    )
    cy.get('.locator-bar')
      .should('be.visible')
      .and('not.have.class', 'locator-bar--vertically-centered')
    cy.findByTestId('locator-bar-icon')
      .should('be.visible')
      .and('have.class', 'cf-icon-svg--bank-round')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Test-Eval-1')
    cy.findByTestId('locator-bar-eyebrow')
      .should('be.visible')
      .and('have.text', 'Evaluator')
  })

  it('displays breadcrumbs', () => {
    cy.mountWithProviders(
      <LocatorBar
        icon='bank-round'
        heading='Home page'
        breadcrumbs={[{ to: '/results', label: 'Back to results' }]}
      />
    )
    cy.get('.locator-bar')
      .should('be.visible')
      .and('have.class', 'locator-bar--vertically-centered')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Home page')
    cy.get('.m-breadcrumbs').should('be.visible')
  })

  it('displays additional content under the heading', () => {
    cy.mount(
      <LocatorBar icon='bank-round' heading='Heading'>
        <p>Extra content</p>
      </LocatorBar>
    )
    cy.get('.locator-bar')
      .should('be.visible')
      .and('not.have.class', 'locator-bar--vertically-centered')
    cy.findByTestId('locator-bar-icon')
      .should('be.visible')
      .and('have.class', 'cf-icon-svg--bank-round')
    cy.findByTestId('locator-bar-heading')
      .should('be.visible')
      .and('have.text', 'Heading')
    cy.findByTestId('locator-bar-subhead')
      .should('be.visible')
      .and('have.text', 'Extra content')
  })
})
