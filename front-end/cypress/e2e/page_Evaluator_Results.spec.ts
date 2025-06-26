import getTableFields from 'pages/Evaluator/results/utils/getTableFields'
import type AccountRecord from 'types/AccountRecord'
import type EvaluatorMetadata from 'types/EvaluatorMetadata'
import type Event from 'types/Event'

import { PII_COOKIE_NAME } from '@src/constants/settings'
import hitsFixture from '../fixtures/evaluatorHits.json'
import eventFixture from '../fixtures/event.json'
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
    cy.get('[data-testid="results-view-toggle"]').should('be.visible')
    cy.get('#sample-tab').should('have.class', 'active')
    cy.get('#all-tab').should('not.have.class', 'active')

    // Sample results message is displayed
    cy.get('[data-testid="results-message"]').should(
      'have.text',
      'Showing 20 sample results'
    )

    // No pagination
    cy.get('.m-pagination').should('not.exist')
  })

  it('Should show full results view after clicking all results button', () => {
    // Navigate to the evaluator page without query params
    page.loadEvaluatorPage()

    // Sample view is indicated in URL and radio button
    cy.location('search').should('include', 'view=sample').and('include', 'page=1')
    cy.get('#sample-tab').should('have.class', 'active')

    // Click all results button
    cy.get('#all-tab').click({ force: true })

    // URL includes view=all
    cy.location('search').should('include', 'view=all').and('include', 'page=1')

    // All results message is displayed
    cy.get('[data-testid="results-message"]').should(
      'include.text',
      'Showing 1 - 20 of 30'
    )

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')
  })

  // it('Should show full results view when view=all is in query params', () => {
  //   page.loadEvaluatorPage('?view=all&page=2')

  //   // All results message is displayed
  //   cy.get('[data-testid="results-message"]').should(
  //     'include.text',
  //     'Showing 21 - 40 of 1,000'
  //   )

  //   // Pagination is added to the page
  //   cy.get('.m-pagination').should('exist')
  //   cy.get('.m-pagination_current-page').should('have.value', '2')
  // })

  // Check that invalid values for valid param keys are replaced
  // const invalidParams = {
  //   '?view=invalid': ['view=sample', 'page=1'],
  //   '?page=num': ['page=1', 'view=sample'],
  //   '?view=unsupported&page=two': ['view=sample', 'page=1'],
  //   '?view=all&page=num': ['view=all', 'page=1'],
  //   '?view=random&page=2': ['view=sample', 'page=1'],
  //   '?view=sample&page=2': ['view=sample', 'page=1']
  // } as const

  // Object.entries(invalidParams).forEach(item => {
  //   it(`Should replace invalid param value in "${item[0]}"`, () => {
  //     page.loadEvaluatorPage(item[0])
  //     cy.location('search').should('not.include', item[0])
  //     item[1].forEach(validParam => {
  //       cy.location('search').should('include', validParam)
  //     })
  //   })
  // })

  it('Should update params after pagination control interaction', () => {
    page.loadEvaluatorPage({ view: 'all' })

    // Pagination is added to the page
    cy.get('.m-pagination').should('exist')
    cy.get('.m-pagination_current-page').should('have.value', '1')

    cy.get('.m-pagination_btn-next').click()
    cy.location('search').should('include', 'page=2')
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
    cy.intercept('GET', 'api/events/1/', { fixture: 'event' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/**`, {
      fixture: 'evaluatorHits'
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
