import { PII_COOKIE_NAME } from '@src/constants/settings'
import { stringifySearchParams } from 'utils/customStringify'

export class EvaluatorPage {
  queryString(params: object) {
    const defaults = { page: 1, page_size: 20, view: 'sample' }
    return stringifySearchParams({ ...defaults, ...params })
  }

  /**
   * Waits for default evaluator page to load with fixture data.
   * @param {object} params - Optional query string params.
   * @param {object} hitsFixture - Optional fixture name.
   * @returns {void} void
   */
  loadEvaluatorPage(params: object = {}, interceptAllHitsPaths = false): void {
    const querystring = this.queryString(params)
    const apiExt = interceptAllHitsPaths ? '**' : `${querystring}`
    const hitsFixture =
      'page' in params && params.page === 2
        ? 'evaluatorHits_page2'
        : 'evaluatorHits_page1'
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/${apiExt}`, {
      fixture: hitsFixture
    }).as('getEvaluatorHits')
    cy.visit(`/events/1/evaluators/Test-Eval-1/${querystring}`)
    cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
  }

  interceptFilteredResults(
    alias: string,
    params: object = {},
    fixture = 'evaluatorHits_page2'
  ): void {
    const querystring = this.queryString(params)
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/${querystring}`, {
      fixture: fixture
    }).as(alias)
  }

  interceptFilteredResultsWithSpy(alias: string, params: object = {}) {
    const querystring = this.queryString(params)

    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-1/${querystring}`,
      cy.spy().as(alias)
    )
  }

  interceptFilteredResultsWithError(
    alias: string,
    params: object = {},
    statusCode = 404
  ) {
    const querystring = this.queryString(params)
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/${querystring}`, {
      statusCode: statusCode,
      body: { error: 'Bad Request' }
    }).as(alias)
  }

  resultsMessage() {
    return cy.get('[data-testid="results-message"]')
  }

  hasResultsMessage(msg: string) {
    this.resultsMessage().should('include.text', msg)
  }

  getNoResultsMessage() {
    return cy.findByTestId('no-results-message')
  }

  getNoResultsClearFiltersLink() {
    return cy.findByTestId('no-results-message__clear-filters')
  }

  hasNoResultsMessage() {
    this.getNoResultsMessage().should('be.visible')
  }

  dofdFalseCheckboxLabel() {
    return cy.get('#dofd_false-label')
  }
  dofdFalseCheckbox() {
    return cy.get('#dofd_false')
  }
  dofdTrueCheckboxLabel() {
    return cy.get('#dofd_true-label')
  }
  dofdTrueCheckbox() {
    return cy.get('#dofd_true')
  }
}
