// export class Metro2Page {
//   breadcrumbs() {
//     return cy.get('.m-breadcrumbs_crumb')
//   }
// }

export function testLocatorBar(eyebrow: string, heading: string) {
  cy.get('.header-with-icon').should('be.visible')
  cy.get('[data-testid="locator-bar-eyebrow"]').should('have.text', eyebrow)
  cy.get('[data-testid="locator-bar-heading"]').should('have.text', heading)
}
