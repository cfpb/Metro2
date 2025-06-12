import { PII_COOKIE_NAME } from 'utils/constants'
export class EvaluatorPage {
  /**
   * Waits for default evaluator page to load with fixture data.
   * @param {string} querystring - Optional query string.
   * @returns {void} void
   */
  loadEvaluatorPage(querystring: string | null = ''): void {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/**`, {
      fixture: 'evaluatorHits'
    }).as('getEvaluatorHits')
    cy.visit(`/events/1/evaluators/Test-Eval-1/${querystring}`)
    cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
  }
}
