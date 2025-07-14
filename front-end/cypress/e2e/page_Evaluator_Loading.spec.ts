/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */
import type Event from 'types/Event'
import hitsFixture from '../fixtures/evaluatorHits_page1.json'
import eventFixture from '../fixtures/event.json'

import { PII_COOKIE_NAME } from '@src/constants/settings'
import AccountRecord from 'types/AccountRecord'
import EvaluatorMetadata from 'types/EvaluatorMetadata'
import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'
import { Metro2Modal } from '../helpers/modalHelpers'
import { Metro2Page } from '../helpers/pageHelper'

// Get data from event fixture
const event: Event = eventFixture

const evaluatorName = 'Test-Eval-1'

// Get evaluator data from event
const evaluator: EvaluatorMetadata = event.evaluators.find(
  item => item.id == evaluatorName
)!

// Get data from hits fixture
const hits: AccountRecord[] = hitsFixture.hits

// Instantiate helpers
const page = new Metro2Page()
const modal = new Metro2Modal()
const evaluatorPage = new EvaluatorPage()

describe('Evaluator page loader', () => {
  it('Should show a loading view while the event data is being fetched', () => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    // Delay the event data
    cy.intercept('GET', `/api/events/1/`, {
      delay: 4000,
      fixture: 'event'
    }).as('getEvent')
    cy.intercept('GET', '/api/users/', {
      delay: 500,
      fixture: 'user'
    }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/${evaluatorName}/**`, {
      delay: 500,
      fixture: 'evaluatorHits_page1'
    }).as('getEvaluatorHits')

    cy.visit(`/events/1/evaluators/${evaluatorName}/`)

    // Loader should be visible on initial visit to evaluator page
    // and page content should be hidden
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('not.exist')
    cy.get('[data-testid="evaluator-summary"]').should('not.exist')
    cy.get('.evaluator-hits-row').should('not.exist')

    // Loader should still be visible and content hidden
    // while event data is still being fetched
    cy.wait(['@getUser', '@getEvaluatorHits'])
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('not.exist')
    cy.get('[data-testid="evaluator-summary"]').should('not.exist')
    cy.get('.evaluator-hits-row').should('not.exist')

    // Content should be visible and loader removed
    // once event data is fetched
    cy.wait('@getEvent')
    cy.get('.loader').should('not.exist')
    cy.get('.locator-bar').should('be.visible')
    cy.get('[data-testid="evaluator-summary"]').should('be.visible')
    cy.get('.evaluator-hits-row').should('be.visible')
  })

  it('Should show a loading view while the user data is being fetched', () => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', `/api/events/1/`, {
      delay: 500,
      fixture: 'event'
    }).as('getEvent')
    // Delay the users data
    cy.intercept('GET', '/api/users/', {
      delay: 4000,
      fixture: 'user'
    }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/${evaluatorName}/**`, {
      delay: 500,
      fixture: 'evaluatorHits_page1'
    }).as('getEvaluatorHits')
    cy.visit(`/events/1/evaluators/${evaluatorName}/`)

    // Loader should be visible on initial visit to evaluator page
    // and evaluator page content should be hidden
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('not.exist')
    cy.get('[data-testid="evaluator-summary"]').should('not.exist')
    cy.get('.evaluator-hits-row').should('not.exist')

    // Loader should still be visible and content hidden
    // while user data is still being fetched
    cy.wait(['@getEvent', '@getEvaluatorHits'])
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('not.exist')
    cy.get('[data-testid="evaluator-summary"]').should('not.exist')
    cy.get('.evaluator-hits-row').should('not.exist')

    // Content should be visible and loader removed
    // once user data is fetched
    cy.wait('@getUser')
    cy.get('.loader').should('not.exist')
    cy.get('.locator-bar').should('be.visible')
    cy.get('[data-testid="evaluator-summary"]').should('be.visible')
    cy.get('.evaluator-hits-row').should('be.visible')
  })

  it('Should show a loading view while the hits data is being fetched', () => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', `/api/events/1/`, {
      fixture: 'event'
    }).as('getEvent')
    cy.intercept('GET', '/api/users/', {
      fixture: 'user'
    }).as('getUser')
    // Delay the hits data
    cy.intercept('GET', `/api/events/1/evaluator/${evaluatorName}/**`, {
      delay: 4000,
      fixture: 'evaluatorHits_page1'
    }).as('getEvaluatorHits')

    cy.visit(`/events/1/evaluators/${evaluatorName}`)

    // Loader should show initially on visit to evaluator page
    // and none of the main content should exist
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('not.exist')
    cy.get('[data-testid="evaluator-summary"]').should('not.exist')
    cy.get('.evaluator-hits-row').should('not.exist')

    // Once user and event data are loaded, locator bar and summary section should
    // be visible, but evaulator hits should still be hidden by a local loader
    cy.wait(['@getUser', '@getEvent'])
    cy.get('.loader').should('be.visible')
    cy.get('.locator-bar').should('be.visible')
    cy.get('[data-testid="evaluator-summary"]').should('be.visible')
    // TODO:
    // cy.get('.evaluator-hits-row').should('not.be.visible')

    // Once evaluator hits are loaded, all content should be visible
    // and loader should be removed
    cy.wait('@getEvaluatorHits')
    cy.get('.loader').should('not.exist')
    // cy.get('.evaluator-hits-row').should('be.visible')
  })
})
