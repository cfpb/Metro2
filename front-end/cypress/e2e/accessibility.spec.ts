/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */
/* eslint-disable */
// @ts-nocheck
import 'cypress-real-events/support'

import { PII_COOKIE_NAME } from '../../src/utils/constants'

import { Metro2Modal } from '../helpers/modalHelpers'

import Event from '../../src/pages/Event/Event'
import eventFixture from '../fixtures/event.json'

// Get data from event fixture
const event: Event = eventFixture
const testEvaluator = event.evaluators[0]
const evaluatorID = testEvaluator.id
const evaluatorDescription = testEvaluator.description

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
    const activeRowEvaluatorID = event.evaluators[1].id
    cy.get('body').realClick()

    // Tab from last cell in first row to first cell in second row,
    // which contains a link to an evaluator
    cy.get('.ag-row')
      .first()
      .within(() => {
        cy.get('.ag-cell').last().realClick().realPress('Tab')
      })

    // Clicking tab in cell with link to evaluator should focus link
    // instead of navigating to next cell
    cy.focused().should('have.text', activeRowEvaluatorID).realPress('Tab')
    cy.focused()
      .should('have.attr', 'href')
      .and('include', `/events/1/evaluators/${activeRowEvaluatorID}`)
  })

  it('Should tab from link in one cell to the next cell', () => {
    const activeRowEvaluator = event.evaluators[1]

    cy.get('body').realClick()
    // Tab from last cell in first row to first cell in second row,
    // which contains a link to an evaluator
    cy.get('.ag-row')
      .first()
      .within(() => {
        cy.get('.ag-cell').last().realClick().realPress('Tab')
      })
    // Clicking tab in first evaluator cell should focus link instead of navigating
    // to next cell
    cy.focused().should('have.text', activeRowEvaluator.id).realPress('Tab')
    cy.focused()
      .should('have.attr', 'href')
      .and('include', `/events/1/evaluators/${activeRowEvaluator.id}`)
      .realPress('Tab')
    // Tabbing away from link in cell should focus next cell
    cy.focused().should('have.text', activeRowEvaluator.description)
  })
})

describe('Modal accessibility', () => {
  describe('Basic modal tests', () => {
    beforeEach(() => {
      cy.viewport(1920, 1080)
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
      cy.intercept('GET', '/api/events/1/evaluator/Status-DOFD-4/**', {
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

    it('Modal should close when escape pressed and reopen when launched again', () => {
      cy.get('body').realClick()
      modal.getModal().should('not.exist')
      // Clicking download button should open download modal
      cy.get('button')
        .contains('Download evaluator results')
        .should('be.visible')
        .click()
      modal.getModal().should('be.visible')
      // Pressing escape should close modal
      cy.realPress('Escape')
      modal.getModal().should('not.be.visible')
      // Clicking download button again should reopen modal after
      // it's been closed by escape button
      cy.get('button').contains('Download evaluator results').click()
      modal.getModal().should('be.visible')
    })
  })

  describe('Required modal test', () => {
    beforeEach(() => {
      cy.viewport(1920, 1080)
      // cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
      cy.visit('/events/1/')
      cy.wait(['@getEvent'])
    })

    it('Should not close modal dialog when escape key is pressed', () => {
      cy.get('body').realClick()
      modal.getModal().should('exist').and('be.visible')
      cy.realPress('Escape')
      modal.getModal().should('be.visible')
    })
  })
})
