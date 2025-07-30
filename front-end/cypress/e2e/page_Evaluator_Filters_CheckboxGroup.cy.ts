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

// Checkbox group helpers
const getCheckedCheckboxesInAccordion = (headerText: string) =>
  page.getExpandableByText(headerText).find('input[type="checkbox"]:checked')

describe('Checkbox group filters', () => {
  beforeEach(() => {
    // Loading the default fixture should show default results message
    evaluatorPage.loadEvaluatorPage({ view: 'all' })
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)

    // Open the account status filter
    page.openExpandable('Account status')
  })

  it('Should apply and remove a single account status filter', () => {
    // Intercept '?acct_stat=11' with 16-result fixture
    evaluatorPage.interceptFilteredResults(
      'currentAccounts', // alias,
      { acct_stat: 11, view: 'all' }, // query params
      'evaluatorHits_16' // fixture to return
    )

    // Account status checkbox should be unchecked
    page.checkboxHasState('Account status', 'unchecked')
    // None of the checkboxes in the account status expandable should be checked
    getCheckedCheckboxesInAccordion('Account status').should('have.length', 0)

    page.openExpandable('Current')

    // Selecting the '11' checkbox in the account status filter
    // should show the 16 results
    page.getExpandableByText('Current').within(() => {
      cy.get('label').contains('11').click()
    })

    // API request for filtered results should be made
    cy.wait('@currentAccounts')

    // URL should contain new query params
    page.hasURL('events/1/evaluators/Test-Eval-1', {
      acct_stat: '11',
      view: 'all'
    })

    // Two checkboxes in Account status accordion should be checked,
    // the one for the 'Current' group and the one for status '11'
    getCheckedCheckboxesInAccordion('Account status').should('have.length', 2)
    page.getExpandableByText('Account status').within(() => {
      page.checkboxHasState('Current', 'checked')
      page.checkboxHasState('11', 'checked')
    })

    // "Account status" checkbox should show indeterminate state
    // since some of its children are checked
    page.checkboxHasState('Account status', 'indeterminate')

    // Results message and table should show 16 results
    evaluatorPage.hasResultsMessage('Showing 1 - 16 of 16 filtered results')
    table.hasRowCount(16)

    // Clicking the 'status 11' checkbox again should remove the filter
    page.getExpandableByText('Current').within(() => {
      cy.get('label').contains('11').click()
    })

    // Query string should not include acct_stat param
    cy.url().should('not.include', 'acct_stat=11').and('not.include', 'acct_stat')

    // Table and message should show 20 results again
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)

    // No account status checkboxes should be checked again
    page.checkboxHasState('Account status', 'unchecked')
    getCheckedCheckboxesInAccordion('Account status').should('have.length', 0)
  })
})
