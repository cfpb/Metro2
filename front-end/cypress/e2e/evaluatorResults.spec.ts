import EvaluatorMetadata from 'pages/Evaluator/Evaluator'
import Event from '../../src/pages/Event/Event'
import { AccountRecord } from '../../src/utils/constants'
import hitsFixture from '../fixtures/evaluatorHits.json'
import eventFixture from '../fixtures/event.json'

import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'
import { Metro2Table } from '../helpers/tableHelpers'

// Get data from event fixture
const event: Event = eventFixture

// Get evaluator data from event
const evaluator: EvaluatorMetadata = event.evaluators.find(
  item => item.id == 'Status-DOFD-4'
)!

// Get data from hits fixture
const hits: AccountRecord[] = hitsFixture.hits

// Instantiate helpers
const page = new EvaluatorPage()
const table = new Metro2Table()

describe('Results view', () => {
  it('Should show the sample results by default', () => {
    // Navigate to the evaluator page without query params
    page.loadEvaluatorPage()

    // view=sample is added to URL
    cy.location('search').should('include', 'view=sample').and('include', 'page=1')

    // Sample view radio is checked
    cy.get('[data-testid="results-view-toggle"]').should('be.visible')
    cy.get('[data-testid="sample-results-button"]').should('have.attr', 'checked')
    cy.get('[data-testid="all-results-button"]').should('not.have.attr', 'checked')

    // Sample results message is displayed
    cy.get('[data-testid="results-message"]').should(
      'have.text',
      `Showing representative sample of ${String(hits.length)} out of ${String(
        evaluator.hits
      )} results`
    )

    // No pagination
    cy.get('.m-pagination').should('not.exist')
  })

  it('Should show full results view after clicking all results button', () => {
    // Navigate to the evaluator page without query params
    page.loadEvaluatorPage()

    // Sample view is indicated in URL and radio button
    cy.location('search').should('include', 'view=sample').and('include', 'page=1')
    cy.get('[data-testid="sample-results-button"]').should('have.attr', 'checked')

    // Click all results button
    cy.get('[data-testid="all-results-button"]').click({ force: true })

    // URL includes view=all
    cy.location('search').should('include', 'view=all').and('include', 'page=1')

    // All results message is displayed
    cy.get('[data-testid="results-message"]').should(
      'include.text',
      `Showing 1-20 of ${String(evaluator.hits)} results`
    )

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    // TODO:
  })

  it('Should show full results view when view=all is in query params', () => {
    page.loadEvaluatorPage('?view=all&page=2')

    // All results message is displayed
    cy.get('[data-testid="results-message"]').should(
      'include.text',
      `Showing 21-40 of ${String(evaluator.hits)} results`
    )

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '2')
  })

  // Check that invalid values for valid param keys are replaced
  const invalidParams = {
    '?view=invalid': ['view=sample', 'page=1'],
    '?page=num': ['page=1', 'view=sample'],
    '?view=unsupported&page=two': ['view=sample', 'page=1'],
    '?view=all&page=num': ['view=all', 'page=1'],
    '?view=random&page=2': ['view=sample', 'page=1'],
    '?view=sample&page=2': ['view=sample', 'page=1']
  } as const

  Object.entries(invalidParams).forEach(item => {
    it(`Should replace invalid param value in "${item[0]}"`, () => {
      page.loadEvaluatorPage(item[0])
      cy.location('search').should('not.include', item[0])
      item[1].forEach(validParam => {
        cy.location('search').should('include', validParam)
      })
    })
  })

  it('Should update params after pagination control interaction', () => {
    page.loadEvaluatorPage('?view=all')

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    cy.get('.m-pagination_btn-next').click()
    cy.location('search').should('include', 'page=2')
  })
})

describe('Results table', () => {
  beforeEach(() => {
    page.loadEvaluatorPage()
  })

  it('Should show correct columns for the evaluator in results table', () => {
    const expectedHeaders = [
      'Account number',
      'Activity date',
      'Account status',
      'DOFD',
      'Payment rating',
      'Amount past due',
      'Compliance condition code',
      'Current balance',
      'Date closed',
      'Original charge-off amount',
      'Scheduled monthly payment amount',
      'Special comment code',
      'Terms frequency'
    ]
    table.verifyHeaders(expectedHeaders)
  })

  it('Should show correct values for each result', () => {
    const fields = [
      'activity_date',
      ...evaluator.fields_used.sort(),
      ...evaluator.fields_display.sort()
    ]

    // verify that the consumer account numbers are displayed for each row
    // in the pinned left column
    table.verifyAccountTableBodyContent(
      table.getPinnedRows(),
      ['cons_acct_num'],
      hits
    )
    // verify that the rest of the fields are displayed for each row
    // in the main table section
    table.verifyAccountTableBodyContent(table.getBodyRows(), fields, hits)
  })
})
