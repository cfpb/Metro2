import { Metro2Modal } from '@cypress/helpers/modalHelpers'
import { PII_COOKIE_NAME } from '@src/constants/settings'
const modal = new Metro2Modal()

describe('Warning modal', () => {
  it('Should show a warning modal when PII cookie is not set', () => {
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.visit('/')
    cy.wait('@getUser')
    // On page load, no PII warning cookie is set
    cy.getCookie(PII_COOKIE_NAME).should('not.exist')

    // Without the cookie, the warning modal is displayed
    modal.getModal('warning-modal').should('exist')
  })

  it('Should set a cookie when warning is accepted', () => {
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.visit('/')
    cy.wait('@getUser')

    // On page load, no PII warning cookie is set
    cy.getCookie(PII_COOKIE_NAME).should('not.exist')

    // The warning modal is displayed
    modal
      .getModal('warning-modal')
      .should('exist')
      .within(() => {
        // Clicking the accept button adds a cookie
        cy.findByTestId('accept-warning-button').click()
        cy.getCookie(PII_COOKIE_NAME).should('have.property', 'value', 'true')
      })
  })
})

it('Should not show a warning modal when PII cookie is set', () => {
  cy.setCookie(PII_COOKIE_NAME, 'true')
  cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
  cy.visit('/')
  cy.wait('@getUser')

  // with the cookie, the warning modal is not displayed
  modal.getModal('warning-modal').should('not.exist')
})
