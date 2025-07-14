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
 * Amount range filters consist of two numerical inputs,
 * one for a min value and the other for a max value.
 */

describe('Evaluator page range amount filters', () => {
  beforeEach(() => {
    // Loading the default fixture should show default results message
    evaluatorPage.loadEvaluatorPage({ view: 'all' })
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)

    // Open the current balance range filter accordion
    page.openExpandable('Current balance')
  })

  it('Should apply and remove amount filters via range inputs', () => {
    // Intercept '?current_bal_min=100' with 16-result fixture
    evaluatorPage.interceptFilteredResults(
      'currentBalMin', // alias,
      { current_bal_min: 100, view: 'all' },
      'evaluatorHits_16' // fixture to return
    )
    // Intercept '?current_bal_min=100&current_bal_max=1000' with 8-result fixture
    evaluatorPage.interceptFilteredResults(
      'currentBalMinMax', // alias
      { current_bal_min: 100, current_bal_max: 1000, view: 'all' }, // query params
      'evaluatorHits_8' // fixture
    )

    // Entering 100 in the current_bal_min field should show 16 results
    cy.get('#current_bal_min').type('100{enter}')
    page.hasURL('events/1/evaluators/Test-Eval-1', {
      current_bal_min: '100',
      view: 'all'
    })
    cy.wait('@currentBalMin')
    cy.get('#current_bal_min').should('have.value', 100)
    evaluatorPage.hasResultsMessage('Showing 1 - 16 of 16 filtered results')
    table.hasRowCount(16)

    // Entering 1000 in the current_bal_max field should show 8 results
    cy.get('#current_bal_max').type('1000{enter}')
    page.hasURL('events/1/evaluators/Test-Eval-1', {
      current_bal_min: '100',
      current_bal_max: '1000',
      view: 'all'
    })
    cy.wait('@currentBalMinMax')
    cy.get('#current_bal_min').should('have.value', 100)
    cy.get('#current_bal_max').should('have.value', 1000)
    evaluatorPage.hasResultsMessage('Showing 1 - 8 of 8 filtered results')
    table.hasRowCount(8)

    // Deleting values in both fields should show original results
    cy.get('#current_bal_max').clear()
    cy.get('#current_bal_min').clear()
    cy.get('#current_bal_max').type('{enter}')
    cy.get('#current_bal_min').should('have.value', '')
    cy.get('#current_bal_max').should('have.value', '')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })

  it('Should remove amount range filter with clear filters link', () => {
    // Intercept '?current_bal_min=100' with 16-result fixture
    evaluatorPage.interceptFilteredResults(
      'currentBalMin', // alias,
      { current_bal_min: 100, view: 'all' },
      'evaluatorHits_16' // fixture to return
    )

    // Entering 100 in the current_bal_min field should show 16 results
    cy.get('#current_bal_min').type('100{enter}')
    page.hasURL('events/1/evaluators/Test-Eval-1', {
      current_bal_min: '100',
      view: 'all'
    })
    cy.wait('@currentBalMin')
    cy.get('#current_bal_min').should('have.value', 100)
    evaluatorPage.hasResultsMessage('Showing 1 - 16 of 16 filtered results')
    table.hasRowCount(16)

    // Clicking the 'remove filters' link should load all the results again
    cy.findByTestId('remove-all-filters').click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { view: 'all' })
    cy.get('#current_bal_min').should('have.value', '')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })

  it('Should show no results message with clear filters link when there are no results', () => {
    // Intercept '?current_bal_min=100' with 0-result fixture
    evaluatorPage.interceptFilteredResults(
      'currentBalMin', // alias,
      { current_bal_min: 100, view: 'all' },
      'evaluatorHits_0' // fixture to return
    )

    // Entering 100 in the current_bal_min field should show no results message
    cy.get('#current_bal_min').type('100{enter}')
    page.hasURL('events/1/evaluators/Test-Eval-1', {
      current_bal_min: '100',
      view: 'all'
    })
    cy.wait('@currentBalMin')
    cy.get('#current_bal_min').should('have.value', 100)
    evaluatorPage.hasResultsMessage('Showing 0 results')
    evaluatorPage.getNoResultsMessage().should('be.visible')

    // Clicking no results message clear filters link should load all results
    evaluatorPage.getNoResultsClearFiltersLink().click()
    page.hasURL('events/1/evaluators/Test-Eval-1', { view: 'all' })
    cy.get('#current_bal_min').should('have.value', '')
    evaluatorPage.hasResultsMessage('Showing 1 - 20 of 30')
    table.hasRowCount(20)
  })
})
