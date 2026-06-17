import { Metro2Modal } from '@cypress/helpers/modalHelpers'
import { stripHtmlTags } from '@cypress/helpers/utils'
import { PII_COOKIE_NAME } from '@src/constants/settings'
const modal = new Metro2Modal()

describe('General page content', () => {
  describe('Warning modal', () => {
    it('Should show a warning modal when PII cookie is not set', () => {
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
      cy.visit('/')
      cy.wait('@getUser')
      // On page load, no PII warning cookie is set
      cy.getCookie(PII_COOKIE_NAME).should('not.exist')

      // Without the cookie, the warning modal is displayed
      modal.getModal('warning-modal').should('exist')

      // The warning modal shows the value of the warning text env variable
      cy.env(['VITE_PII_WARNING_TEXT']).then(({ VITE_PII_WARNING_TEXT }) => {
        modal
          .getModal('warning-modal')
          .should('be.visible')
          .within(() => {
            cy.findByTestId('warning-text')
              .should('exist')
              .and('include.text', stripHtmlTags(VITE_PII_WARNING_TEXT as string))
          })
      })
    })

    it('Should set a cookie when PII warning is accepted', () => {
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

    it('Should not show a warning modal when PII cookie is set', () => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
      cy.visit('/')
      cy.wait('@getUser')

      // with the cookie, the warning modal is not displayed
      modal.getModal('warning-modal').should('not.exist')
    })
  })

  describe('Page header', () => {
    it('Should show a page header based on env variable', () => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
      cy.visit('/')
      cy.wait('@getUser')

      cy.env(['VITE_SHOW_CFPB_HEADER']).then(({ VITE_SHOW_CFPB_HEADER }) => {
        if (VITE_SHOW_CFPB_HEADER === 'true') {
          // CFPB header should show
          cy.get('.o-header')
            .should('be.visible')
            .within(() => {
              cy.get('.o-header__logo').should('exist')
              cy.get('.nav-items')
                .should('have.length', 1)
                .first()
                .should('have.text', 'User guide')
            })
        } else {
          // Default header should show
          cy.get('header[data-testid="metro2-header"]')
            .should('be.visible')
            .within(() => {
              cy.get('h1').should('have.text', 'Metro2 Evaluator Tool')
              cy.get('.links')
                .should('have.length', 1)
                .first()
                .should('have.text', 'Need help? See the user guide')
            })
        }
      })
    })
  })
})
