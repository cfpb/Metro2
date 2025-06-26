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
   * @returns {void} void
   */
  loadEvaluatorPage(params?: object): void {
    const querystring = params ? this.queryString(params) : ''
    const apiExt = querystring ? `${querystring}` : '**'
    const urlExt = querystring ? `${querystring}` : ''
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/${apiExt}`, {
      fixture: 'evaluatorHits'
    }).as('getEvaluatorHits')
    cy.visit(`/events/1/evaluators/Test-Eval-1/${urlExt}`)
    cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
  }

  interceptFilteredResults(
    alias: string,
    params: object = {},
    fixture: string = 'evaluatorHits'
  ): void {
    const querystring = this.queryString(params)
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-1/${querystring ? querystring : ''}`,
      {
        fixture: fixture
      }
    ).as(alias)
  }

  interceptFilteredResultsWithSpy(alias: string, params: object = {}) {
    const querystring = this.queryString(params)
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-1/${querystring ? querystring : ''}`,
      cy.spy().as(alias)
    )
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
    return cy.findByTestId('no-results-message_clear-filters')
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
