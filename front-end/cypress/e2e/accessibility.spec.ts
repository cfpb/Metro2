/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */
/* eslint-disable */
// @ts-nocheck
import 'cypress-real-events/support'

import { PII_COOKIE_NAME } from '../../src/utils/constants'

import { Metro2Modal } from '../helpers/modalHelpers'

// Instantiate helpers
const modal = new Metro2Modal()

describe('Table accessibility', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
    cy.visit('/events/1/')
    cy.wait(['@getEvent'])
  })

  it('Should have keyboard-accessible links in tables', () => {
    cy.get('body').realClick()
    // Tab to first evaluator cell in table from last cell in header row
    cy.get('.ag-header-cell').last().realClick().realPress('Tab')
    // Clicking tab in first evaluator cell should focus link
    // instead of navigating to next cell
    cy.focused().should('have.text', 'Status-Balance-1').realPress('Tab')
    cy.focused()
      .should('have.attr', 'href', '/events/1/evaluators/Status-Balance-1')
      .realClick()
    cy.location('pathname').should('eq', '/events/1/evaluators/Status-Balance-1')
  })

  it('Should tab from link in one cell to the next cell', () => {
    cy.get('body').realClick()
    // Click into last header cell and tab to Evaluator id cell in first body row
    cy.get('.ag-header-cell').last().realClick().realPress('Tab')
    // Clicking tab in first evaluator cell should focus link instead of navigating
    // to next cell
    cy.focused().should('have.text', 'Status-Balance-1').realPress('Tab')
    cy.focused()
      .should('have.attr', 'href', '/events/1/evaluators/Status-Balance-1')
      .realPress('Tab')
    // Tabbing away from link in cell should focus next cell
    cy.focused().should(
      'have.text',
      'Account status indicates that the account was transferred, paid, or closed, but there is a current balance.'
    )
  })
})

describe('Modal accessibility', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', '/api/events/1/evaluator/Status-DOFD-4/', {
      fixture: 'evaluatorHits'
    }).as('getEvaluatorHits')
    cy.visit('/events/1/evaluators/Status-DOFD-4/')
    cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
  })

  it('Should allow keyboard navigation of interactive elements in modal', () => {
    cy.get('body').realClick()
    modal.getModal().should('not.exist')
    cy.get('button')
      .contains('Download evaluator results')
      .should('be.visible')
      .click()
    modal.getModal().should('be.visible')
    // When the modal opens, its first interactive element should be focused
    cy.focused()
      .should('have.attr', 'name', 'evaluator-download')
      .and('have.id', 'sample')
    // Pressing the down arrow should select the other radio button
    cy.realPress('ArrowDown')
    cy.focused()
      .should('have.attr', 'name', 'evaluator-download')
      .and('have.id', 'all')
    // Tabbing should go to the PII checkbox
    cy.realPress('Tab')
    cy.focused()
      .should('have.attr', 'name', 'confirmPII')
      .and('have.attr', 'aria-checked', 'false')
    // Pressing space bar should check the checkbox
    cy.realPress('Space')
    cy.focused()
      .should('have.attr', 'name', 'confirmPII')
      .and('have.attr', 'aria-checked', 'true')
    // Tabbing should go to links in PII text
    cy.realPress('Tab')
    cy.focused().should('have.text', 'Service Center')
    cy.realPress('Tab')
    cy.focused().should('have.text', 'privacy@cfpb.gov')
    // Tabbing again should go to save button
    cy.realPress('Tab')
    cy.focused().should('contain.text', 'Save file')
  })

  it('Should prevent modal dialog from closing when escape key is pressed', () => {
    cy.get('body').realClick()
    modal.getModal().should('not.exist')
    cy.get('button')
      .contains('Download evaluator results')
      .should('be.visible')
      .click()
    modal.getModal().should('be.visible')
    cy.realPress('Escape')
    modal.getModal().should('be.visible')
  })
})
