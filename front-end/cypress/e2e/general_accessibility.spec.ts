/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */
/* eslint-disable */
// @ts-nocheck
import 'cypress-real-events/support'

import { PII_COOKIE_NAME } from '@src/constants/settings'

import { Metro2Modal } from '../helpers/modalHelpers'

import type Event from 'types/Event'
import eventFixture from '../fixtures/event.json'

// Get data from event fixture
const event: Event = eventFixture

// Instantiate helpers
const modal = new Metro2Modal()

describe('Table accessibility', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/154/', { fixture: 'event' }).as('getEvent')
    cy.visit('/events/154/')
    cy.wait(['@getEvent'])
  })

  it('Should have keyboard-accessible links in tables', () => {
    const testEvaluator = event.evaluators[0]
    const evaluatorID = testEvaluator.id
    const evaluatorDescription = testEvaluator.description

    cy.get('body').realClick()
    // On the event results page, tabbing from last cell in table header
    // should focus first cell in first table body row,
    // which contains a link to the first evaluator with hits.
    cy.get('.ag-header-cell').last().click(1, 1)
    cy.realPress('Tab')
    cy.focused().should('have.text', evaluatorID)
    // Tabbing again should focus the link itself instead of
    // navigating to the next cell
    cy.realPress('Tab')
    cy.focused()
      .should('have.text', evaluatorID)
      .and('have.attr', 'href')
      .and('include', `/events/1/evaluators/${evaluatorID}`)
    // Tabbing again should focus the next cell
    cy.realPress('Tab')
    cy.focused().should('have.text', evaluatorDescription)
  })
})

describe('Modal accessibility', () => {
  describe('Basic modal tests', () => {
    beforeEach(() => {
      cy.viewport(1920, 1080)
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
      cy.intercept('GET', '/api/events/1/evaluator/Test-Eval-1/**', {
        fixture: 'evaluatorHits_page1'
      }).as('getEvaluatorHits')
      cy.visit('/events/1/evaluators/Test-Eval-1/')
      cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
    })

    it('Should allow keyboard navigation of interactive elements in modal', () => {
      cy.get('body').realClick()
      modal.getModal().should('not.exist')
      cy.get('button').contains('Save results').should('be.visible').click()
      modal.getModal().should('be.visible')
      // When the modal opens, its first interactive element should be focused
      // Close button is focused
      cy.focused().should('contain.text', 'Close')
      // Tabbing should bring you to the copy url button
      cy.realPress('Tab')
      cy.focused().should('contain.text', 'Copy URL')
      // Tabbing should bring you to the PII checkbox
      // cy.realPress('Tab')
      // cy.focused()
      //   .should('have.attr', 'name', 'confirmPII')
      //   .and('have.attr', 'aria-checked', 'false')
      // // Pressing space bar should check the checkbox
      // cy.realPress('Space')
      // cy.focused()
      //   .should('have.attr', 'name', 'confirmPII')
      //   .and('have.attr', 'aria-checked', 'true')
      // Tabbing again should go to save button
      // cy.realPress('Tab')
      // cy.focused().should('contain.text', 'Save file')
    })

    it('Modal should close when escape pressed and reopen when launched again', () => {
      cy.get('body').realClick()
      modal.getModal().should('not.exist')
      // Clicking download button should open download modal
      cy.get('button').contains('Save results').should('be.visible').click()
      modal.getModal().should('be.visible')
      // Pressing escape should close modal
      cy.realPress('Escape')
      modal.getModal().should('not.be.visible')
      // Clicking download button again should reopen modal after
      // it's been closed by escape button
      cy.get('button').contains('Save results').click()
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
