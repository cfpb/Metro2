import getTableFields from 'pages/Evaluator/results/utils/getTableFields'
import type AccountRecord from 'types/AccountRecord'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'

import { PII_COOKIE_NAME } from '@src/constants/settings'
import hitsFixture from '../fixtures/evaluatorHits_page1.json'
import eventFixture from '../fixtures/event_1.json'
import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'
import { Metro2Table } from '../helpers/tableHelpers'

const evaluatorName = 'Test-Eval-1'

// Get data from event fixture
const event: Event = eventFixture

// Get evaluator data from event
const evaluator: EvaluatorMetadata = event.evaluators.find(
  item => item.id == evaluatorName
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

    // Sample view tab is active
    cy.get('.tabbed_navigation').should('be.visible')
    cy.findByTestId('sample-results-tab').should('have.class', 'active')
    cy.findByTestId('all-results-tab').should('not.have.class', 'active')

    // Sample results message is displayed
    cy.findByTestId('results-message').should(
      'have.text',
      'Showing 20 sample results'
    )

    // No pagination
    cy.get('.m-pagination').should('not.exist')
  })

  it('Should show full results view after clicking all results button', () => {
    // Navigate to the evaluator page without query params
    page.loadEvaluatorPage()

    // Sample view is indicated in URL and tab
    cy.location('search').should('include', 'view=sample').and('include', 'page=1')
    cy.findByTestId('sample-results-tab').should('have.class', 'active')

    // Intercept all results request
    page.interceptFilteredResults(
      'allResults',
      { view: 'all' },
      'evaluatorHits_page1'
    )

    // Click all results button
    cy.findByTestId('all-results-tab').click({ force: true })

    cy.wait(['@allResults'])

    // URL includes view=all
    cy.location('search').should('include', 'view=all').and('include', 'page=1')

    // All results message is displayed
    cy.findByTestId('results-message').should('include.text', 'Showing 1 - 20 of 30')

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    // Table shows 20 rows
    table.hasRowCount(20)
  })

  it('Should show full results view when view=all is in query params', () => {
    page.loadEvaluatorPage({ view: 'all' })

    // All results message is displayed
    cy.findByTestId('results-message').should('include.text', 'Showing 1 - 20 of 30')

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    // Table shows 20 rows
    table.hasRowCount(20)
  })

  it('Should show second page of results when page 2 is in query params', () => {
    page.loadEvaluatorPage({ view: 'all', page: 2 })

    // Page 2 results message is displayed
    cy.findByTestId('results-message').should(
      'include.text',
      'Showing 21 - 30 of 30'
    )

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '2')

    // Table shows 10 rows
    table.hasRowCount(10)
  })

  it('Should update params after pagination control interaction', () => {
    page.loadEvaluatorPage({ view: 'all' })

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    // All results message is displayed
    cy.findByTestId('results-message').should('include.text', 'Showing 1 - 20 of 30')
    // Table shows 20 rows
    table.hasRowCount(20)

    // Intercept page 2 request
    page.interceptFilteredResults(
      'page2',
      { page: 2, view: 'all' },
      'evaluatorHits_page2'
    )

    // Click next button to navigate to page 2
    cy.get('.m-pagination_btn-next').click()

    cy.wait(['@page2'])

    // Page 2 appears in querystring
    cy.location('search').should('include', 'page=2')

    // Updated results message is displayed
    cy.findByTestId('results-message').should(
      'include.text',
      'Showing 21 - 30 of 30'
    )
    // Table shows 10 rows
    table.hasRowCount(10)
  })
})

describe('Invalid param handling', () => {
  // Check that invalid values for valid param keys are replaced
  const invalidParams = {
    '?view=invalid': ['view=sample', 'page=1'],
    '?page=num': ['page=1', 'view=sample'],
    '?view=unsupported&page=two': ['view=sample', 'page=1'],
    '?view=all&page=num': ['view=all', 'page=1'],
    '?view=random&page=2': ['view=sample', 'page=1'],
    '?view=sample&page=2': ['view=sample', 'page=1']
  } as const

  beforeEach(() => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/**`, {
      fixture: 'evaluatorHits_page1'
    }).as('getEvaluatorHits')
  })

  Object.entries(invalidParams).forEach(item => {
    it(`Should replace invalid param value in "${item[0]}"`, () => {
      cy.visit(`/events/1/evaluators/Test-Eval-1/${item[0]}`)
      cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
      cy.location('search').should('not.include', item[0])
      item[1].forEach(validParam => {
        cy.location('search').should('include', validParam)
      })
    })
  })
})

describe('Error handling', () => {
  it('Should navigate to page 1 when request 404s', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    // intercept 24 with error
    page.interceptFilteredResultsWithError('page24', { page: 24, view: 'all' }, 404)
    // intercept page 1
    page.interceptFilteredResults(
      'page1',
      { page: 1, view: 'all' },
      'evaluatorHits_page1'
    )
    cy.visit(`/events/1/evaluators/Test-Eval-1/?view=all&page=24`)
    cy.wait(['@page1'])
    cy.location('search')
      .should('include', 'view=all')
      .and('not.include', 'page=24')
      .and('include', 'page=1')
  })

  // it('Should show error message in table when other error received', () => {
  //   cy.viewport(1920, 1800)
  //   cy.setCookie(PII_COOKIE_NAME, 'true')
  //   cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
  //   cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
  //   // intercept 2 with error
  //   page.interceptFilteredResultsWithError('page2', { page: 2, view: 'all' }, 500)
  //   cy.visit(`/events/1/evaluators/Test-Eval-1/?view=all&page=2`)
  //   cy.wait(20000)
  //   cy.location('search')
  //     .should('include', 'view=all')
  //     .and('not.include', 'page=1')
  //     .and('include', 'page=2')
  //   page.getNoResultsMessage().should('be.visible')
  // })
})

describe('Results table', () => {
  beforeEach(() => {
    page.loadEvaluatorPage()
  })

  it('Should show correct columns for the evaluator in results table', () => {
    const expectedHeaders = [
      'Account number',
      'Activity date',
      'Current balance',
      'DOFD',
      'Terms frequency',
      'Account status',
      'Payment rating',
      'Payment history profile',
      'Payment history profile (most recent entry)',
      'Special comment code',
      'Compliance condition code',
      'Amount past due',
      'Date of account information',
      'Date closed',
      'Bankruptcy - Consumer information indicator for account holder',
      'Bankruptcy - Consumer information indicator for associated consumers',
      'Account change indicator (L1)'
    ]
    table.verifyHeaders(expectedHeaders)
  })

  it('Should show correct values for each result', () => {
    // verify that the consumer account numbers are displayed for each row
    // in the pinned left column
    table.verifyAccountTableBodyContent(
      table.getPinnedRows(),
      ['cons_acct_num'],
      hits
    )
    // verify that the rest of the fields are displayed for each row
    // in the main table section
    const fields = getTableFields(evaluator.fields_used, evaluator.fields_display)
    // remove consumer account number because it's in a separate section
    fields.shift()
    table.verifyAccountTableBodyContent(table.getBodyRows(), fields, hits)
  })
})
