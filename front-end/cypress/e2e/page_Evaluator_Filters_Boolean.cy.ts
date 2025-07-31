/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */

import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'
import { Metro2Page } from '../helpers/pageHelper'
import { Metro2Table } from '../helpers/tableHelpers'

// Instantiate helpers
const page = new Metro2Page()
const evaluatorPage = new EvaluatorPage()
const table = new Metro2Table()

/**
 * Boolean filters consist of two checkboxes that allow a user
 * to filter for cases where a field has a value and ones where it doesn't.
 *
 * Both options (populated & blank) can be selected,
 * which is effectively the same as neither option being selected.
 * In that situation, a filter value of field_name=any is added to the URL
 * but no filter for the field is included in the API request.
 */

describe('Evaluator page boolean filters', () => {
  beforeEach(() => {
    // Loading the default fixture should show default results message
    evaluatorPage.loadEvaluatorPage({ view: 'all' })
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)

    // Open the DOFD boolean filter accordion
    page.openExpandable('Date of first delinquency (DOFD)')
  })

  /**
   * This test verifies that
   *   1. checking one box
   *       - URL: adds field_name=true or field_name=false to querystring
   *       - API: sends field_name=true or field_name=false in request
   *       - UI: updates the page with filtered data from API
   *   2. checking both boxes
   *       - URL: adds field_name=any
   *       - API: removes field_name from query
   *              no request is made since results without this filter are stored
   *       - UI: updates the page with all data from react-query storage
   *   3. unchecking one box when both are checked
   *       - URL: field_name=still checked value in querystring
   *       - API: sends the still selected filter value in request
   *       - UI: updates the page with filtered data from API
   *   4. unchecking only checked box
   *       - URL: removes field_name
   *       - API: removes field_name from query
   *              no request is made since results without this filter are stored
   *       - UI: updates the page with all data from react-query storage
   */
  it('Should apply and remove boolean filters with checkboxes', () => {
    // Intercept '?dofd=false' with 8-result fixture
    evaluatorPage.interceptFilteredResults(
      'noDofdResults', // alias,
      { dofd: 'false', view: 'all' },
      'evaluatorHits_8' // fixture to return
    )
    // Intercept '?dofd=true' with 16-result fixture
    evaluatorPage.interceptFilteredResults(
      'hasDofdResults', // alias
      { dofd: 'true', view: 'all' }, // query params
      'evaluatorHits_16' // fixture
    )
    // Intercept '?dofd=any' with spy
    evaluatorPage.interceptFilteredResultsWithSpy(
      'anyDofdResults', // alias
      { dofd: 'any', view: 'all' } // query params
    )

    // Clicking the 'no DOFD' filter checkbox should show 8 results
    evaluatorPage.dofdFalseCheckboxLabel().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { dofd: 'false', view: 'all' })
    cy.wait('@noDofdResults')
    evaluatorPage.dofdFalseCheckbox().should('be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 8 of 8 filtered results')
    table.hasRowCount(8)

    // Selecting both filter options should load all results from react-query storage
    // and not call API with dofd query param
    evaluatorPage.dofdTrueCheckboxLabel().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { dofd: 'any', view: 'all' })
    cy.get('@anyDofdResults').should('not.been.called')
    evaluatorPage.dofdFalseCheckbox().should('be.checked')
    evaluatorPage.dofdTrueCheckbox().should('be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)

    // De-selecting the 'no DOFD' checkbox should show 16 results
    evaluatorPage.dofdFalseCheckboxLabel().click()
    cy.wait(['@hasDofdResults'])
    page.hasURL('events/1/evaluators/Test-Eval-1', { dofd: 'true', view: 'all' })
    evaluatorPage.dofdFalseCheckbox().should('not.be.checked')
    evaluatorPage.dofdTrueCheckbox().should('be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 16 of 16 filtered results')
    table.hasRowCount(16)

    // Removing all the dofd filters should load original results from react-query
    evaluatorPage.dofdTrueCheckboxLabel().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { view: 'all' })
    evaluatorPage.dofdFalseCheckbox().should('not.be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })

  it('Should remove boolean filter with clear filters link', () => {
    // Intercept '?dofd=false' with 8-result fixture
    evaluatorPage.interceptFilteredResults(
      'noDofdResults', // alias
      { dofd: 'false', view: 'all' }, // query params
      'evaluatorHits_8' // fixture to return
    )

    // Clicking 'no dofd' filter checkbox should show 8 results
    evaluatorPage.dofdFalseCheckboxLabel().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { dofd: 'false', view: 'all' })
    cy.wait('@noDofdResults')
    evaluatorPage.dofdFalseCheckbox().should('be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 8 of 8 filtered results')
    table.hasRowCount(8)

    // Clicking the 'remove filters' link should load all the results again
    cy.findByTestId('remove-all-filters').click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { view: 'all' })
    evaluatorPage.dofdFalseCheckbox().should('not.be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })

  it('Should show no results message with clear filters link when there are no results', () => {
    // Intercept '?dofd=false' with 0-result fixture
    evaluatorPage.interceptFilteredResults(
      'noDofdResults', // alias
      { dofd: 'false', view: 'all' }, // query params
      'evaluatorHits_0' // fixture to return
    )

    // Clicking no dofd checkbox should show no results message
    evaluatorPage.dofdFalseCheckboxLabel().click()
    cy.wait('@noDofdResults')
    page.hasURL('events/1/evaluators/Test-Eval-1', { dofd: 'false', view: 'all' })
    evaluatorPage.dofdFalseCheckbox().should('be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 0 results')
    evaluatorPage.getNoResultsMessage().should('be.visible')

    // Clicking no results message clear filters link should load all results
    evaluatorPage.getNoResultsClearFiltersLink().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { view: 'all' })
    evaluatorPage.dofdFalseCheckbox().should('not.be.checked')
    evaluatorPage.dofdTrueCheckbox().should('not.be.checked')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })
})
